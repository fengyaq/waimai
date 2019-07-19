//获取应用实例
var app = getApp();
Page({
    data: {
        "content":"",
        "score":10,
        // "order_sn":""
    },
    onLoad: function (e) {
        console.log(e)
        this.setData({
            order_sn: e.id
        })
    },
    onShow:function(e){

    },
    scoreChange:function( e ){
        this.setData({
            "score":e.detail.value
        });
    },
    inputchange:function(e){
        this.setData({
            content:e.detail.value
        })
    },


    doComment:function(){
        var that = this;
        wx.request({
            url: app.buildUrl("/v1/comment/add"),
            method:'POST',
            header: app.getRequestHeader(),
            data:{
                order_sn:that.data.order_sn,
                score:that.data.score,
                content:that.data.content
            },
            success: function (res) {
                var res = res.data;
                if (res.code != 1) {
                    app.alert({"content": res.msg});
                    return;
                }
                 wx.navigateBack({
                    delta:-1
                })
            }
        });
    },

});