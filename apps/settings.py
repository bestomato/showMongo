#-*- coding:utf-8 -*-

# installed app list 
INSTALLED_APPS = (
    'home',
    'user',
)

#  static file config
#  if application debug is true:
#      static_url is maked by application settings static_path
#  if application debug is false:
#      if cdn is true:
#          static url is cdn
#      if cdn is false:
#          static url is maked by application settings static_path
CDN = {
    'is': False,
    'host': 'http://s.androidesk.com/aoi'
}


# response code reflect response result after server process request  
#
#
#
#
#
