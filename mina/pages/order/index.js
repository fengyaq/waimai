//获取应用实例
var app = getApp();

Page({
    data: {
        ids:[],
        goods_list:[],
        address_id:0,
        note:'',
         // 接收前端传递的id num fromtype
        // fromtype=1&id=3&num=3
        id:0,
        num:0,


        // goods_list: [
            // {
            //     id:22,
            //     name: "小鸡炖蘑菇",
            //     price: "85.00",
            //     pic_url: "/images/food.jpg",
            //     number: 1,
            // },
            // {
            //     id:22,
            //     name: "小鸡炖蘑菇",
            //     price: "85.00",
            //     pic_url: "/images/food.jpg",
            //     number: 1,
            // }
        // // ],
        // default_address: {
        //     name: "编程浪子",
        //     mobile: "12345678901",
        //     detail: "上海市浦东新区XX",
        // },
        // yun_price: "1.00",
        // pay_price: "85.00",
        // total_price: "86.00",
        params: null,

    },
    onShow: function () {
        var that = this;
        // that.getOrderList()
    },
    // onLoad: function (e) {
    //     // var ids = JSON.parse(e.ids);
    //     // console.log(ids);
    //     var that = this;
    //     that.setData({
    //         ids:JSON.parse(e.ids)
    //     });
    //     that.getOrderInfo();
    //     console.log('ok');
    // },
    // 如果使用同一个订单接口 使用fromtype做区别
    // 默认是从购物车端的提交订单fromtype=0
    // fromtype=1时是从商品详情的立即购买提交订单
    onLoad:function(e){
        console.log(e);
        var that=this;
        // 获取标识fromtype
        var fromtype =e.fromtype;
        console.log(e.fromtype);
        that.setData({
            fromtype:fromtype
        });
        if (fromtype =='0'){
            var ids=JSON.parse(e.ids);
            console.log(ids);
            that.setData({
                ids:ids,
            });
            that.getOrderInfo()
        }
        if (fromtype =='1'){
            var id=e.id;
            var num=e.num;
            var fromtype =e.fromtype;
            console.log(e.fromtype);
            that.setData({
                id:id,
                num:num,
                fromtype:fromtype
            });
            that.getOrderIndex()
        }
    },

    getInput:function(e){
        // console.log(e.detail.value)
        this.setData({
            note:e.detail.value
        })
    },
    createOrder: function (e) {
        // wx.showLoading();
        var that = this;
        wx.request({
            url: app.buildUrl('/v1/order/create'),
            method: 'POST',
            data: {
                'ids': JSON.stringify(that.data.ids),
                'address_id':that.data.address_id,
                'note':that.data.note
            },
            header: app.getRequestHeader(),
            success(res) {
                console.log(res.data);
                if (res.data.code != 1) {
                    //     app.alert({'content': res.data.msg});
                    //     return
                }
                //重定向跳转页面
                wx.redirectTo({
                    url:'/pages/my/order_list'
                })
            }
        })
    },
    addressSet: function () {
        wx.navigateTo({
            url: "/pages/my/addressSet"
        });
    },
    selectAddress: function () {
        wx.navigateTo({
            url: "/pages/my/addressList"
        });
    },


    getOrderInfo:function () {
        var that = this;
        wx.request({
            url: app.buildUrl('/v1/order/commit'),
            method: 'POST',
            data: {
                'ids': JSON.stringify(that.data.ids),
                'address_id':that.data.address_id,
                'note':that.data.note
            },
            header: app.getRequestHeader(),
            success(res) {
                if (res.data.code != 1) {
                    //     app.alert({'content': res.data.msg});
                    //     return
                }
                that.setData({
                    goods_list: res.data.data.goods_list,
                    default_address: res.data.data.default_address,
                    yun_price: res.data.data.yun_price,
                    pay_price: res.data.data.pay_price,
                    total_price: res.data.data.total_price,
                    address_id:res.data.data.default_address.id
                });
                // console.log(res.data.data.foods);

            }
        })

    },
      // 立即购买提交订单去结算页面
    getOrderIndex: function () {
        var that = this;
        wx.request({
            url: app.buildUrl('/v1/order/info'),
            method: 'POST',
            data: {
                // 取出id和Num
                id:that.data.id,
                num:that.data.num
            },
            header: app.getRequestHeader(),
            success(res) {
                if (res.data.code != 1) {
                    app.alert({'content': res.data.msg});
                    return
                }
                that.setData({
                    goods_list: res.data.data.goods_list,
                    default_address: res.data.data.default_address,
                    address_id: res.data.data.default_address.id,
                    yun_price: res.data.data.yun_price,
                    pay_price: res.data.data.pay_price,
                    total_price: res.data.data.total_price,
                })
            }
        })
    }
});

