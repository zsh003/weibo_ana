
from django.contrib import admin
from django.urls import path
from myadmin.views import views,admin_user,user

urlpatterns = [

    # 浏览器访问的 url

    path('', views.login,name="myadmin_login"),
    path('login', views.login,name="myadmin_login2"),
    path('dologin', views.dologin,name="myadmin_dologin"),
    path('logout', views.logout,name="myadmin_logout"),
    path('register', views.register,name="myadmin_register"),
    path('doregister', views.doregister,name="myadmin_doregister"),

    path('admin_user/<int:pIndex>', admin_user.index,name="myadmin_user_index"),
    path('admin_user/add', admin_user.add,name="myadmin_user_add"),
    path('admin_user/insert', admin_user.insert,name="myadmin_user_insert"),
    path('admin_user/edit<int:uid>', admin_user.edit,name="myadmin_user_edit"),
    path('admin_user/update<int:uid>', admin_user.update,name="myadmin_user_update"),


    # 展示用户历史搜索记录
    path('user/historyList<int:uid>', user.historyList, name= "user_showHistory"),
    path('user/delete<int:uid>', user.delete_search_history, name="user_delete"),
    path('user/getSearchIndex', user.search_index, name="user_search_index"),
    path('user/getSearch', user.doSearch, name="user_doSearch"),
    # 个人信息
    path('user/index<int:uid>', user.user_index, name="user_index"),
    path('user/edit<int:uid>', user.user_edit, name="user_edit"),
    path('user/update<int:uid>', user.user_update, name="user_update"),


    path('', views.wordCloud,name="home"),
    path('index',views.index,name="index"),
    path('wordCloud', views.wordCloud, name="wordCloud"), # 生成词云图
    path('getAreaPriceIndex', views.getAreaPriceIndex, name="getAreaPriceIndex"),
    path('drawAreaPrice', views.drawAreaPrice, name="drawAreaPrice"),
    path('getAreaPriceData', views.getAreaPriceData, name="getAreaPriceData"),
    path('getSearchIndex', views.getSearchIndex, name="getSearchIndex"),
    path('doOpitionSearch', views.doOpitionSearch, name="doOpitionSearch"),
    path('getOpinionIndex', views.getOpinionIndex, name="getOpinionIndex"),

    # 获取绘制饼图数据接口
    path('getSearchPieData', views.getSearchPieData, name="getSearchPieData"),
    path('drawSearchPie', views.drawSearchPie, name="drawSearchPie"),


    path('drawMap', views.drawMap, name="drawMap"),
    path('couldWord', views.couldWord, name="couldWord"),
    path('getMapData', views.getMapData, name="getMapData"),
    path('weiboTiezi', views.weiboTiezi, name="weiboTiezi"),
    path('weiboPinglun', views.weiboPinglun, name="weiboPinglun"),
    path('weiboYujing<int:uid>', views.weiboYujing, name="weiboYujing"),
    path('doOpitionSearch1', views.doOpitionSearch1, name="doOpitionSearch1"),

    path('drawPredict', views.drawPredict, name="drawPredict"),
    path('getPredictData', views.getPredictData,name="getPredictData"),



]
