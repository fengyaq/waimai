var app = getApp();
Page({
    data: {
        list: [
            // {
            //     date: "2018-07-01 22:30:23",
            //     order_number: "20180701223023001",
            //     content: "记得周六发货",
            // },
            // {
            //     date: "2018-07-01 22:30:23",
            //     order_number: "20180701223023001",
            //     content: "记得周六发货",
            // }
        ]
    },
    onLoad: function (options) {
        // 生命周期函数--监听页面加载

    },
    onShow: function () {
        var that = this;
        this.getCommentList()
    },
    // 我的评论页面
    getCommentList: function () {
        var that = this
        wx.request({
            url: app.buildUrl('/v1/comment/list1'),
            method: 'GET',
            header: app.getRequestHeader(),
            success: function (res) {
                var data = res.data
                if (data.code != 1) {
                    app.alert({'content': data.msg})
                    return;
                }

                that.setData({
                    list: data.data.list
                })
            }

        })

    }


});
