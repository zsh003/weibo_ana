from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q   

from myadmin.models import User



def index(request,pIndex=1):
    umod=User.objects
    ulist=umod.filter(status__lt=9)
    mywhere=[]  
    kw=request.GET.get("keyword",None)
    if kw:
        ulist=ulist.filter(Q(username__contains=kw)|Q(nickname__contains=kw)) 
        mywhere.append('keyword='+kw)
    pIndex=int(pIndex)
    page=Paginator(ulist,50) 
    maxPages=page.num_pages  
    if pIndex>maxPages:
        pIndex=maxPages
    if pIndex<1:
        pIndex=1
    list2=page.page(pIndex) 
    plist=page.page_range
    context={"userlist":list2,'plist':plist,'pIndex':pIndex,'maxPages':maxPages,'mywhere':mywhere}
    return render(request,'myadmin/user/index.html',context)

def add(request):
    return render(request,"myadmin/user/add.html")

def insert(request):
    try:
        ob = User()
        ob.username = request.POST['username']
        ob.nickname = request.POST['nickname']
        ob.phone = request.POST['phone']
        if request.POST['password'] == request.POST['repassword']:
            import re
            if bool(re.match(r'^1[3-9]\d{9}$',ob.phone)) == True:
                import hashlib,random
                md5=hashlib.md5()
                n=random.randint(100000,999999)
                s=request.POST['password']+str(n)
                md5.update(s.encode('utf-8'))
                ob.password_hash=md5.hexdigest()
                ob.password_salt=n
                ob.status=6
                ob.create_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ob.update_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ob.save()
                context={'info':'添加成功'}
            else:
                context={'info':'手机号格式错误'}
        else:
            context={'info':'两次输入密码不一致'}
    except Exception as err:
        print(err)
        context = {'info': '添加失败'}
    return render(request,'myadmin/info.html',context)


def edit(request,uid=0):
    try:
        ob = User.objects.get(id=uid)
        context = {'user': ob}
        return render(request, 'myadmin/user/edit.html', context)
    except Exception as e:
        print(e)
        context = {'info': '没有找到信息'}
        return render(request, 'myadmin/info.html', context)
def update(request,uid):
    try:
        ob = User.objects.get(id=uid)
        ob.nickname=request.POST['nickname']
        ob.phone = request.POST['phone']
        ob.status=request.POST['status']
        ob.update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        import re
        if bool(re.match(r'^1[3-9]\d{9}$',ob.phone)) == True:
            ob.save()
            context = {'info': '修改成功'}
        else:
            context = {'info': '手机号格式错误'}
    except Exception as e:
        print(e)
        context = {'info': '修改失败'}
    return render(request, 'myadmin/info.html', context)