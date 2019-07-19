//index.js
//获取应用实例
var app = getApp();
Page({
    data: {
        indicatorDots: true,
        autoplay: true,
        interval: 3000,
        duration: 1000,
        loadingHidden: false, // loading
        swiperCurrent: 0,
        categories: [],
        activeCategoryId: 0,
        goods: [],
        scrollTop: "0",
        loadingMoreHidden: true,
        searchInput: '',
        banners: [],
        page:1,
        ismore:1,
        isloading:false
    },
    onLoad: function () {
        var that = this;

        wx.setNavigationBarTitle({
            title: app.globalData.shopName
        });

        that.setData({
            banners: [
            //     {
            //         "id": 1,
            //         "pic_url": "/images/food.jpg"
            //     },
            //     {
            //         "id": 2,
            //         "pic_url": "/images/food.jpg"
            //     },
            //     {
            //         "id": 3,
            //         "pic_url": "/images/food.jpg"
            //     }
            // ],
            // categories: [
            //     {id: 0, name: "全部"},
            //     {id: 1, name: "川菜"},
            //     {id: 2, name: "东北菜"},
            // ],
            // activeCategoryId: 0,
			// goods: [
			//                 {
			//                     "id": 1,
			//                     "name": "小鸡炖蘑菇-1",
			//                     "min_price": "15.00",
			//                     "price": "15.00",
			//                     "pic_url": "/images/food.jpg"
			//                 },
			//                 {
			//                     "id": 2,
			//                     "name": "小鸡炖蘑菇-1",
			//                     "min_price": "15.00",
			//                     "price": "15.00",
			//                     "pic_url": "/images/food.jpg"
			//                 },
			//                 {
			//                     "id": 3,
			//                     "name": "小鸡炖蘑菇-1",
			//                     "min_price": "15.00",
			//                     "price": "15.00",
			//                     "pic_url": "/images/food.jpg"
			//                 },
			//                 {
			//                     "id": 4,
			//                     "name": "小鸡炖蘑菇-1",
			//                     "min_price": "15.00",
			//                     "price": "15.00",
			//                     "pic_url": "/images/food.jpg"
			//                 }
            //
			 ],
            // loadingMoreHidden: false
        });
        //调用获取数据
        that.getBannersAndCategories()
        that.getFoods()
    },
    scroll: function (e) {
        var that = this, scrollTop = that.data.scrollTop;
        that.setData({
            scrollTop: e.detail.scrollTop
        });
    },

    //事件处理函数
    swiperchange: function (e) {
        this.setData({
            swiperCurrent: e.detail.current
        })
    },
	listenerSearchInput:function( e ){
	        this.setData({
	            searchInput: e.detail.value
	        });
	 },
	 toSearch:function( e ){
	        this.setData({
	            p:1,
	            goods:[],
	            loadingMoreHidden:true
	        });
	        this.getFoodList();
	},
    tapBanner: function (e) {
        if (e.currentTarget.dataset.id != 0) {
            wx.navigateTo({
                url: "/pages/food/info?id=" + e.currentTarget.dataset.id
            });
        }
    },
    toDetailsTap: function (e) {
        console.log(e)
        wx.navigateTo({
            url: "/pages/food/info?id=" + e.currentTarget.dataset.id
        });
    },
    onReachBottom:function(){
        console.log('到底部了')
        var that = this
        if (that.data.isloading==false){
            if (that.data.ismore!=0){
            that.setData({
                page:that.data.page+1
            })
            that.getFoods()
        }
        }

    },
    //点击e,e就是哪个view
    cateclick:function(e){
        var that = this
        console.log(e.target.id)
        that.setData({
            activeCategoryId:e.target.id,
            goods:[],
            page:1
        })
        //    点击分类重新获取数据
        that.getFoods()
    },
    getBannersAndCategories:function () {
        var that = this
        wx.request({
            url: app.buildUrl('/v1/food/search'),
            method: 'GET',
            header: app.getRequestHeader(),
            success(res) {
                // console.log(res.data)
                if (res.data.code == -1){
                    app.alert({
                        'content':res.data.data.msg
                            })
                    return
                }
                // if (res.data.code == 1) {
                that.setData({
                    'banners':res.data.data.banners,
                    'categories':res.data.data.categories
                    })
                // }
            }
        })
    },
    getFoods:function () {

        var that = this
        that.setData({
            'isloading':true
        })
        wx.request({
            url: app.buildUrl('/v1/food/all'),
            method: 'GET',
            data:{
                'cid':that.data.activeCategoryId,
                'page':that.data.page
            },
            header: app.getRequestHeader(),
            success(res) {
                // console.log(res.data)
                //concat和push区别
                if (res.data.code == -1){
                    app.alert({
                        'content':res.data.data.msg
                            })
                    return
                }
                // if (res.data.code == 1) {
                that.setData({
                    'goods':that.data.goods.concat(res.data.data.goods),
                    'ismore':res.data.data.ismore,
                    'isloading':false
                })
                if (that.data.ismore==0){
                    that.setData({
                        loadingMoreHidden:false
                    })
                    // }
                }
            }
        })
    }

});
