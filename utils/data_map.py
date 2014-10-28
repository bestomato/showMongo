#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime

# 充分利用mongodb batch insert的特性，加快数据导入速度

DEFAULT_LIMIT = 10000


def data_transfer(old_db, new_db, o2n, skip=0, limit=0):
    max_limit = old_db.count()

    def func1(old_db, new_db, o2n, skip):
        while skip < max_limit:
            l = []
            for i in old_db.find(skip=skip, limit=DEFAULT_LIMIT, sort=[('_id', 1)]):
                l.append(o2n({}, i))

            if l:
                print 'func1 skip ', skip
                new_db.create(l)
            skip += DEFAULT_LIMIT

    def func2():
        cursor = old_db.find(sort=[('_id', 1)])
        count = 0
        total = cursor.count()

        l = []
        for i in cursor:
            l.append(o2n({}, i))
            count += 1
            if count % 10000 == 0:
                print 'func2 count %s %d / %d' % (datetime.datetime.now(), count, total)
                new_db.create(l)
                l = []
        if l:
            new_db.create(l)

    # func1(old_db, new_db, o2n, skip)
    func2()


def data_filter_transfer(load_old, new_db, o2n, *args, **kwargs):
    l = []
    for i in load_old(*args, **kwargs):
        l.append(o2n({}, i))

    if l:
        new_db.create(l)


def run(func_list, **kwargs):
    import time
    import datetime

    start = time.time()
    module_name = kwargs.get('globals', {}).get('__name__', '')
    print 'start ', module_name, ' transfer'
    print '\n'
    for i in func_list:
        print '-----------'
        print datetime.datetime.now(), ' start %s transfer' % i
        eval('%s_transfer()' % i, kwargs.get('globals', globals()))
        print datetime.datetime.now(), ' end %s transfer' % i

    print '\n'
    print 'consume total %s seconds' % (time.time() - start)
    print 'end ', module_name, ' transfer'