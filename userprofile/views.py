from userprofile.models import Profile
from userprofile.forms import ProfileForm, UserLoginForm, UserRegisterForm
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User


# 登陆
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


# 登出
def user_logout(request):
    logout(request)
    return redirect('blog:index')


# 注册
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


# 编辑用户信息
def profile_edit(request, id):
    user = User.objects.get(id=id)
    # user_id 是 OneToOneField 自动生成的字段
    # profile = Profile.objects.get(user_id=id)
    if Profile.objects.filter(user_id=id).exists():
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile.objects.create(user=user)

    if request.method == "POST":
        # 验证修改数据者，是否为用户本人
        if request.user != user:
            return HttpResponse('你没有权限修改此用户信息~')

        # 上传的文件保存在 request.FILES 中，通过参数传递给表单类
        profile_form = ProfileForm(data=request.POST, files=request.FILES)
        if profile_form.is_valid():
            profile_cd = profile_form.cleaned_data
            profile.phone = profile_cd['phone_number']
            profile.bio = profile_cd['bio']
            # 如果 request.FILES 存在文件，则保存
            if 'avatar' in request.FILES:
                profile.avatar = profile_cd['avatar']
            profile.save()
            return redirect('userprofile:profile_edit', id=id)
        else:
            return HttpResponse('注册表单输入有误。请重新输入~')
    elif request.method == "GET":
        profile_form = ProfileForm()
        context = {
            'profile_form': profile_form,
            'profile': profile,
            'user': user,
        }
        return render(request, 'userprofile/edit.html', context)
    else:
        return HttpResponse('请使用GET或POST请求数据~')
