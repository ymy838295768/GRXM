import uuid

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.cache import cache
from App.models import UserModel, SecondRcommend, SecondCollection


def home(request):
    data = {
        "title":"Rock",
    }
    second = SecondRcommend.objects.all()
    data['second'] = second
    return render(request,'home/home.html',context=data)

def s_l(request):

    is_login = False

    user_id = request.session.get('user_id')

    data = {
        'title': '已登录',
        'is_login': is_login,
    }
    if user_id:
        try:
            user = UserModel.objects.get(pk=user_id)
            is_login = True
            data['is_login'] = is_login
            data['user_icon'] = '/' + user.u_icon.url
            data['user_name'] = user.u_name

            second = SecondRcommend.objects.all()
            data['second'] = second

        except Exception as e:
            print(str(e))

    return render(request, 'home_logined/home_logined.html', context=data)


def s_l_c(request):
    is_login = False
    user_id = request.session.get('user_id')
    data = {
        'title': '已登录',
        'is_login': is_login,
    }
    if user_id:
        try:
            user = UserModel.objects.get(pk=user_id)
            is_login = True
            data['is_login'] = is_login
            data['user_icon'] = '/' + user.u_icon.url
            data['user_name'] = user.u_name
            secondcollections = SecondCollection.objects.filter(user_id=user_id)
            if secondcollections:
                data['collections'] =secondcollections
        except Exception as e:
            print(str(e))

        return render(request,'home_logined_collected/home_logined_collected.html',context=data)

def login(request):
    if request.method == "GET":
        msg = request.session.get('msg')
        data ={
            'title':'用户登录',
        }
        if msg:
            data['msg'] = msg
        return render(request, 'login/login.html',context=data)
    elif request.method == "POST":
        username = request.POST.get('u_name')
        password = request.POST.get('u_password')

        users = UserModel.objects.filter(u_name=username)
        if users.exists():
            user = users.first()
            if user.check_password(password):
                    request.session['user_id'] = user.id
                    return redirect(reverse('second:home_logined'))
            else:
                request.session['msg'] = '账户或密码错误'
                return redirect(reverse('second:login'))
        else:
            request.session['msg'] = '账户或密码错误'
            return redirect(reverse('second:login'))

def register(request):
    if request.method == "GET":
        data = {
            'title': '用户注册',
        }
        return render(request, 'register/register.html', context=data)
    elif request.method == "POST":
        u_name = request.POST.get("u_name")
        u_email = request.POST.get("u_email")
        u_password = request.POST.get("u_password")
        u_password2 = request.POST.get("u_password2")
        u_icon = request.FILES.get("u_icon")

        if u_password == u_password2:
            user = UserModel()
            user.u_name = u_name
            user.u_email = u_email
            user.u_icon = u_icon
            user.set_password(u_password)
            print("save")

            user.save()

            request.session['user_id'] = user.id

            token = str(uuid.uuid4())
            cache.set(token, user.id)

            return redirect(reverse('second:home_logined'))
        else:
            return render(request,'register/register.html')

def u_i(request):
    if request.method == "GET":
        data = {
            'title': '用户信息修改',
        }
        return render(request, 'userinfo_mod/userinfo_mod.html', context=data)
    elif request.method == "POST":
        u_password = request.POST.get("u_password")
        u_email = request.POST.get("u_email")
        u_icon = request.FILES.get("u_icon")

        user_id = request.session.get('user_id')
        try :
            if user_id:
                user = UserModel.objects.get(pk=user_id)
                user.set_password(u_password)
                user.u_email = u_email
                user.u_icon = u_icon
                user.save()
        except Exception as e:
            print(str(e))

        return redirect(reverse('second:home_logined'))


def logout(request):
    request.session.flush()
    return redirect(reverse('second:home'))

def collect(request):
    second = request.GET.get('second')
    print(second)
    userid = request.session.get('user_id')
    data = {
        'status':'200',
        'msg' : 'ok',
    }
    if not userid:
        data['status'] = '404'
    else:
        secondcollection = SecondCollection.objects.filter(second_id=second).filter(user_id=userid)
        if secondcollection.exists():
            secondcollection.delete()
        else:
            data['status'] = '201'
            secondcollectioni = SecondCollection()
            secondcollectioni.user_id_id= userid
            secondcollectioni.second_id_id = second
            secondcollectioni.save()

    return JsonResponse(data)

