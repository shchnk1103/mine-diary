from userprofile.forms import UserLoginForm, UserRegisterForm
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse


def user_login(request):
    if request.method == "GET":
        user_login_form = UserLoginForm()
        context = {
            'form': user_login_form
        }
        return render(request, 'userprofile/login.html', context)

    elif request.method == "POST":
        user_login_form = UserLoginForm(data=request.POST)

        if user_login_form.is_valid():
            data = user_login_form.cleaned_data
            user = authenticate(
                username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return redirect('blog:index')
            else:
                return HttpResponse('账号密码输入有误，请重新输入～')
        else:
            return HttpResponse('账号密码不合法，请重试～')
    else:
        return HttpResponse('请使用GET或POST请求数据~')


def user_logout(request):
    logout(request)
    return redirect('blog:index')


def user_register(request):
    if request.method == "POST":
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            # 设置密码
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            # 注册好后直接登陆并跳转到主页
            login(request, new_user)
            return redirect('blog:index')
        else:
            return HttpResponse('注册时输入有误，请重新输入～')
    elif request.method == "GET":
        user_register_form = UserRegisterForm()
        context = {
            'form': user_register_form
        }
        return render(request, 'userprofile/register.html', context)
    else:
        return HttpResponse('请使用GET或POST请求数据~')
