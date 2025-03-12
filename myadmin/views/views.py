import csv
import json

import pymysql
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.db import connection
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from matplotlib import pyplot as plt
from pmdarima import ARIMA
from wordcloud import WordCloud
import numpy
import PIL.Image as Image
from snownlp import SnowNLP

from myadmin import models
from myadmin.models import User, Comment,search_history
from datetime import datetime
from django.utils.safestring import mark_safe
from django.shortcuts import render
import pandas as pd
from django.http import JsonResponse
from pmdarima.arima import auto_arima






# 登录界面
def login(request):
    return render(request, 'login.html')


# 登录
def dologin(request):
    try:
        user = User.objects.get(username=request.POST['username'])
        if user.status == 1:
            import hashlib
            md5 = hashlib.md5()
            s = request.POST['pass'] + user.password_salt
            md5.update(s.encode('utf-8'))
            if user.password_hash == md5.hexdigest():
                # 登录成功
                request.session['user'] = user.toDict()
                warning_info = SentimentClass(user.keyword, user.Threshold)
                if '警告' in warning_info:
                    context = {'warning_info': warning_info, 'keyword': user.keyword, 'Threshold': user.Threshold}
                    return render(request, 'weiboYujing.html', context)
                else:
                    # 重定向
                    return redirect(reverse("index"))
            else:
                context = {"info": '提示：密码错误'}
        if user.status == 6:
            import hashlib
            md5 = hashlib.md5()
            s = request.POST['pass'] + user.password_salt
            md5.update(s.encode('utf-8'))
            if user.password_hash == md5.hexdigest():
                # 登录成功
                request.session['adminuser'] = user.toDict()
                # 重定向
                return redirect(reverse("myadmin_user_index", args=(1,)))
            else:
                context = {"info": '提示：密码错误'}
        else:
            context = {"info": '提示：帐号被管理员禁用'}
    except Exception as e:
        print(e)
        context = {"info": '提示：帐号不存在'}
    return render(request, 'login.html', context)


# 登出
def logout(request):
    request.session.clear()
    return HttpResponseRedirect('login')


# 注册界面
def register(request):
    return render(request, 'register.html')


# 注册
def doregister(request):
    ob = User()
    username = request.POST['username']
    phone = request.POST['phone']
    password = request.POST['password']
    password1 = request.POST['password1']
    nickname = request.POST['nickname']
    if password == password1:
        import hashlib, random
        md5 = hashlib.md5()
        n = random.randint(100000, 999999)
        s = request.POST['password'] + str(n)
        md5.update(s.encode('utf-8'))
        ob.username = username
        ob.password_hash = md5.hexdigest()
        ob.password_salt = n
        ob.status = 1
        ob.phone = phone
        ob.nickname = nickname
        ob.create_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        info = '注册成功！'
        context = {'info': info}
        return render(request, 'login.html', context)
    else:
        info = '两次密码不一致！'
        context = {'info': info}
        return render(request, 'register.html', context)


# 首页
def index(request):
    return render(request, 'index.html')

# 生成词云图，并存为图片
def wordCloud(search):
    # 建立一个数据库游标
    cur0 = connection.cursor()
    # 获取数据库表comment中每条评论
    sql = "SELECT comment FROM comment where comment !='' and keyword like '%" + search + "%'"
    cur0.execute(sql)
    datas0 = cur0.fetchall()
    # 遍历所有结果，print(datas)
    word_list = ''
    for data in datas0:
        word_list += data[0] + ','
    # print(word_list)，获取数据库comment表中用户的昵称
    sql2 = ''' SELECT DISTINCT screen_name from comment '''
    cur0.execute(sql2)
    datas00 = cur0.fetchall()
    for data in datas00:
        word_list += data[0] + ','
    with open('test.txt', 'w', encoding='utf-8') as file:
        file.write(word_list)
    with open("test.txt", encoding="utf-8") as file:
        text = file.read()
        # 打开名称为1的图片，将其转化为numpy数组格式，存储在mask_pic变量中，用作词云形状
        mask_pic = numpy.array(Image.open("./static/img/1.jpg"))
        wordcloud = WordCloud(font_path="C:/Windows/Fonts/simfang.ttf", mask=mask_pic,
                              background_color='white').generate(text)
        image = wordcloud.to_image()
        image.save('./static/img/wc.jpg')


# 情感分类函数
def SentimentClass(search,Threshold):
    positive = 0
    mid = 0
    midup = 0
    negative = 0
    cur1 = connection.cursor()
    sql = "SELECT comment FROM comment where comment !='' and keyword like '%" + search + "%'"
    cur1.execute(sql)
    datas1 = cur1.fetchall()
    # 采用SnowNLP库进行情感判断
    for data in datas1:
        s1 = SnowNLP(data[0])
        score = s1.sentiments
        if score >= 0 and score <= 0.3:
            negative += 1
        elif score > 0.3 and score <= 0.5:
            mid += 1
        elif score > 0.5 and score <= 0.8:
            midup += 1
        else:
            positive += 1
    warning_info = '关键词：'+search + '；            暂无警报'
    if negative > int(Threshold):
        warning_info = '关键词：'+search+'；           警告：负面舆情预警'
    return warning_info


# 展示评论函数
def showComment(search):
    cur2 = connection.cursor()
    sql2 = "select * from  comment WHERE keyword like '%" + search + "%' ORDER BY like_count DESC LIMIT 30"
    cur2.execute(sql2)
    datas2 = cur2.fetchall()
    x_data = []
    for data2 in datas2:
        temp = {}
        temp['screen_name'] = data2[3]
        temp['comment'] = data2[4]
        temp['source'] = data2[5]
        temp['like_count'] = data2[6]
        x_data.append(temp)
    return x_data


# 展示帖子函数
def showSearch(search):
    cur3 = connection.cursor()
    sql3 = "select * from  search WHERE keyword like '%" + search + "%' ORDER BY comments_count DESC"
    cur3.execute(sql3)
    datas3 = cur3.fetchall()
    y_data = []
    for data3 in datas3:
        temp = {}
        temp['screen_name'] = data3[3]
        temp['text'] = mark_safe(data3[9])
        temp['city'] = data3[7]
        temp['comments_count'] = data3[5]
        temp['attitudes_count'] = data3[6]
        y_data.append(temp)
    return y_data

# 保存用户搜索记录函数
def insertHistory(uid,search):
    ob = search_history()
    ob.uid = uid
    ob.seaHistory = search
    ob.created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ob.save()




def getAreaPriceIndex(request):
    return render(request, 'getAreaPriceIndex.html')


def drawAreaPrice(request):
    return render(request, 'drawAreaPrice.html')


def getAreaPriceData(request):
    global search
    cur = connection.cursor()
    sql = "SELECT screen_name,like_count FROM comment where keyword like '%" + search + "%' ORDER BY RAND() LIMIT 10"
    cur.execute(sql)
    datas = cur.fetchall()
    get_lg_data_x = []
    get_lg_data_y = []

    for data in datas:
        get_lg_data_x.append(data[0])
        get_lg_data_y.append(int(data[1]))
    context = {'get_lg_data_x': get_lg_data_x, 'get_lg_data_y': get_lg_data_y}
    print(context)
    return JsonResponse(context)


def getSearchIndex(request):
    return render(request, 'getSearchIndex.html')


def drawSearchPie(request):
    # 介绍饼图
    z_data = explainPie(search)
    return render(request, 'drawSearchPie.html',{'z_data':z_data})

def couldWord(request):
    return render(request, 'couldWord.html')

def weiboTiezi(request):
    # 展示该关键词所有帖子
    y_data = showSearch(search)
    return render(request, 'weiboTiezi.html', {'y_data':y_data})

def weiboPinglun(request):
    # 展示该关键词的所有点赞量前20评论
    x_data = showComment(search)
    return render(request, 'weiboPinglun.html', {'x_data':x_data})

def weiboYujing(request,uid):
    user = models.User.objects.get(id=uid)
    # 判断负面情绪是否超过阈值
    warning_info = SentimentClass(user.keyword, user.Threshold)
    if '警告' in warning_info:
        context = {'warning_info': warning_info, 'keyword': user.keyword, 'Threshold': user.Threshold}
        return render(request, 'weiboYujing.html', context)
    else:
        context = {'warning_info': warning_info, 'keyword': user.keyword,
                   'Threshold': user.Threshold}
        return render(request, 'weiboYujing.html', context)



# 执行查询关键词操作
@csrf_exempt
def doOpitionSearch1(request):
    search = request.POST['keyword']
    Threshold = request.POST['Threshold']  # 传递阈值
    # 介绍饼图
    z_data = explainPie(search)
    # 展示该关键词所有帖子
    y_data = showSearch(search)
    # 展示该关键词的所有点赞量前20评论
    x_data = showComment(search)
    # 判断负面情绪是否超过阈值
    warning_info = SentimentClass(search, Threshold)
    # 生成词云图
    wordCloud(search)
    if request.session.is_empty():
        context = {'warning_info': warning_info, 'x_data': x_data, 'y_data': y_data,'z_data': z_data,}
        return render(request, 'drawSearchPie.html', context)
    else:
        context = {'warning_info': warning_info, 'x_data': x_data, 'y_data': y_data,'z_data': z_data, "isVisit": '1'}
        return render(request, 'drawSearchPie.html', context)


search=''
# 执行查询关键词操作
def doOpitionSearch(request):
    global search, Threshold
    uid = request.POST['uid']
    search = request.POST['search']
    # Threshold = request.POST['Threshold']  # 传递阈值
    # 保存用户的搜索记录
    insertHistory(uid,search)
    # 介绍饼图
    z_data = explainPie(search)
    # 展示该关键词所有帖子
    y_data = showSearch(search)
    # 展示该关键词的所有点赞量前20评论
    x_data = showComment(search)
    # 判断负面情绪是否超过阈值
    # warning_info = SentimentClass(search, Threshold)
    # 生成词云图
    wordCloud(search)
    if request.session.is_empty():
        context = { 'x_data': x_data, 'y_data': y_data,'z_data': z_data,}
        return render(request, 'drawSearchPie.html', context)
    else:
        context = { 'x_data': x_data, 'y_data': y_data,'z_data': z_data, "isVisit": '1'}
        return render(request, 'drawSearchPie.html', context)


# 封装要介绍的情感数据
def explainPie(search):
    positive = 0
    mid = 0
    midup = 0
    negative = 0
    cur = connection.cursor()
    sql = "SELECT comment FROM comment where comment !='' and keyword like '%" + search + "%'"
    cur.execute(sql)
    datas = cur.fetchall()
    for data in datas:
        s1 = SnowNLP(data[0])
        score = s1.sentiments
        if score >= 0 and score <= 0.3:
            negative += 1
        elif score > 0.3 and score <= 0.5:
            mid += 1
        elif score > 0.5 and score <= 0.8:
            midup += 1
        else:
            positive += 1
    z_data = []
    temp = {}
    temp['positive'] = positive
    temp['mid'] = mid
    temp['midup'] = midup
    temp['negative'] = negative
    temp['search'] = search
    z_data.append(temp)
    return z_data

# 得到绘画情感饼图的数据
def getSearchPieData(request):
    global search
    positive = 0
    mid = 0
    midup = 0
    negative = 0
    cur = connection.cursor()
    sql = "SELECT comment FROM comment where comment !='' and keyword like '%" + search + "%'"
    cur.execute(sql)
    datas = cur.fetchall()
    for data in datas:
        s1 = SnowNLP(data[0])
        score = s1.sentiments
        if score >= 0 and score <= 0.3:
            negative += 1
        elif score > 0.3 and score <= 0.5:
            mid += 1
        elif score > 0.5 and score <= 0.8:
            midup += 1
        else:
            positive += 1
    x_data = []
    temp1 = {'value': positive, 'name': '积极'}
    temp2 = {'value': mid, 'name': '较好'}
    temp3 = {'value': midup, 'name': '普通'}
    temp4 = {'value': negative, 'name': '消极'}
    x_data.append(temp1)
    x_data.append(temp2)
    x_data.append(temp3)
    x_data.append(temp4)
    context = {'x_data': x_data}
    return JsonResponse(context)


def getOpinionIndex(request):
    positive = 0
    mid = 0
    midup = 0
    negative = 0
    cur = connection.cursor()
    sql = "SELECT comment FROM comment where comment !=''"
    cur.execute(sql)
    datas = cur.fetchall()
    for data in datas:
        s1 = SnowNLP(data[0])
        score = s1.sentiments
        if score >= 0 and score <= 0.3:
            negative += 1
        elif score > 0.3 and score <= 0.5:
            mid += 1
        elif score > 0.5 and score <= 0.8:
            midup += 1
        else:
            positive += 1
    return render(request, 'getSearchIndex.html')


def drawMap(request):
    return render(request, 'drawMap.html')

def getMapData(request):
    cur = connection.cursor()
    query = """ SELECT REPLACE(source, '来自', '') AS new_status_province, COUNT(*) 
                    FROM comment 
                    WHERE keyword LIKE %s 
                    GROUP BY new_status_province 
                    UNION ALL
                    SELECT status_province, COUNT(*) 
                    FROM search 
                    WHERE keyword LIKE %s 
                    GROUP BY status_province """
    cur.execute(query, ('%' + search + '%', '%' + search + '%'))
    rows = cur.fetchall()
    counts = {}
    for row in rows:
        province = row[0]
        count = row[1]
        if province not in counts:
            counts[province] = 0
        counts[province] += count
    out = [{'name': province, 'value': count} for province, count in counts.items()]
    context = {'x_data': out, 'search': search}
    return JsonResponse(context)



def drawPredict(request):
    return render(request, 'drawPredict.html')

def getPredictData(request):
    # 绘画预测
    import random
    # 随机生成1到4之间的整数
    random_number = random.randint(1, 4)
    # 将数字和文件名字符串连接起来，形成随机的文件名
    filename = str(random_number) + ".csv"
    print(random_number)
    # with open(f"D:/aaaa/weibo_view_web/myadmin/views/{filename}") as f:

    with open(f"./myadmin/views/{filename}") as f:
    # with open(f"C:/Users/83852/Desktop/weibo_view_web/myadmin/views/{filename}") as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]
         # 获取X和Y数据
    x_data = [datetime.strptime(row['date'], '%Y/%m/%d %H:%M') for row in data]
    y_data1 = [(row['real']) for row in data]
    y_data2 = [(row['fit']) for row in data]
    y_data3 = [(row['predict']) for row in data]
    # 封装数据为JSON格式
    chart_data = {
        'x_data': x_data,
        'y_data1': y_data1,
        'y_data2': y_data2,
        'y_data3': y_data3
    }
    # 转换为JSON格式并返回
    return JsonResponse(chart_data)

