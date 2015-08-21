// 删除数据
var coll=$(".delete-coll-data");
coll.on("click", function(){
    var div=$(this).attr("data-div");
    var url=$(this).attr("data-href");

    swal({
            title: "您确定要删除么?",
            text: "",
            type: "warning",
            cancelButtonText: "取消",
            showCancelButton: true,
            showButtonText: '确定',
            confirmButtonColor: '#ca3c3c',
            confirmButtonText: '确定',
            closeOnConfirm: false
        },
        function(){
            $.get(url, function(data){
                if(data.data === "yes"){
                    swal('删除成功','','success');
                    $("#"+div).slideUp("fast");
                }
            });
        }
    );

});


// 清空数据
$(".clear_coll").on("click", function(){
    var url=$(this).attr("data-href");

    swal({
            title: "您确定要清空数据表么?",
            text: "",
            type: "warning",
            cancelButtonText: "取消",
            showCancelButton: true,
            showButtonText: '确定',
            confirmButtonColor: '#ca3c3c',
            confirmButtonText: '确定',
            closeOnConfirm: false
        },
        function(){
            $.get(url, function(data){
                if(data.data === 'yes'){
                    swal('删除成功','','success');
                    window.location.href="/record?db={{ dbs_value }}&coll={{ coll_value }}";
                }
            });
        }
    );
});