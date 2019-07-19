var app = getApp();
Page({
    data: {
        statusType: ["待付款", "待发货", "待收货", "待评价", "已完成","已关闭"],
        status:[ "-8","-7","-6","-5","1","0" ],
        currentType: 0,
        tabClass: ["", "", "", "", "", ""]
    },
    statusTap: function (e) {
        var curType = e.currentTarget.dataset.index;
        this.data.currentType = curType;
        this.setData({
            currentType: curType
        });
        this.onShow();
    },
    orderDetail: function (e) {
        wx.navigateTo({
            url: "/pages/my/order_info"
        })
    },
    onLoad: function (options) {
        // 生命周期函数--监听页面加载

    },
    onReady: function () {
        // 生命周期函数--监听页面初次渲染完
    },
    onShow: function () {
        var that = this;
        that.getOrderList()
        that.setData({
            order_list: [
                // {
				// 	status: -8,
                //     status_desc: "待支付",
                //     date: "2018-07-01 22:30:23",
                //     order_number: "20180701223023001",
                //     note: "记得周六发货",
                //     total_price: "85.00",
                //     goods_list: [
                //         {
                //             pic_url: "/images/food.jpg"
                //         },
                //         {
                //             pic_url: "/images/food.jpg"
                //         }
                //     ]
                // }
            ],

        });
    },
    onHide: function () {
        // 生命周期函数--监听页面隐藏

    },
    onUnload: function () {
        // 生命周期函数--监听页面卸载

    },
    onPullDownRefresh: function () {
        // 页面相关事件处理函数--监听用户下拉动作

    },
    onReachBottom: function () {
        // 页面上拉触底事件的处理函数

    },
    getOrderList:function () {
        var that = this;
        wx.request({
            url: app.buildUrl('/v1/order/list'),
            method: 'GET',
            data: {
                'status':this.data.status[this.data.currentType]
            },
            header: app.getRequestHeader(),
            success(res) {
                if (res.data.code == -1) {
                    //     app.alert({'content': res.data.msg});
                    //     return
                }
                that.setData({
                    order_list: res.data.data.order_list
                });
                // console.log(res.data.data.foods);

            }
        })
    },
    goComment:function (e) {
        console.log(e)
        // 跳转到评论页，订单的路径
        wx.navigateTo({
            url:'/pages/my/comment?id='+e.currentTarget.dataset.id
        })
    },
    getOrderInfo:function(){
        var that = this;
        wx.request({
            url:app.buildUrl('/v1/order/info'),
            method:'POST',
            data:{
                'id':that.data.id,
                'num':that.data.num,
            },
            header:app.getRequestHeader(),
            success(res) {
                if(res.data.code == -1){
                    // app.alter({'content':res.data.msg})
                    return
                }
                that.setData({
                    goods_list:res.data.data.goods_list,
                    default_address:res.data.data.default_address,
                    address_id:res.data.data.default_address.id,
                    yun_price: res.data.data.yun_price,
                    pay_price:res.data.data.pay_price,
                    total_price: res.data.data.total_price,
                })
            }
        })
    },

});
