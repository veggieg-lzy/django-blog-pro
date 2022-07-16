# users/views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render,HttpResponse,redirect

from users.forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm,UserForm,UserProfileForm

#邮箱注册导入库  ModelBackend是Django使用的默认身份验证后端
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from users.models import EmailVerifyRecord
from utils.email_send import send_register_email

# 引入用户模型字段
from .models import UserProfile
from django.contrib.auth.decorators import login_required

# 本视图登录后才能访问，所以检测登录的装饰器一定要加
@login_required(login_url='users:login')   # 设置登录后才能访问，如果没有登陆，就跳转到login界面
def user_profile(request):
    user = User.objects.get(username=request.user)#获取该用户
    return render(request, 'users/user_profile.html', {'user': user})



def login_view(request):
    # if request.method=='POST':
    #     username=request.POST['username'] #后面的username参数是来自前端html中定义的表单
    #     password=request.POST['password']# request.POST[]或request.POST.get()获取数据
    #     #print(username,password)
    #     # 与数据库中的用户名和密码比对，django默认保存密码是以哈希形式存储，并不是明文密码，这里的password验证默认调用的是User类的check_password方法，以哈希值比较。
    #     user = authenticate(request, username=username, password=password)
    #     if user is not None:
    #         # 验证如果用户不为空
    #         #login方法登录
    #         login(request,user)#内置登录函数
    #         return HttpResponse('登录成功') #在网页中返回登陆成功
    #     else:
    #         # 返回登录失败信息
    #         return HttpResponse('登陆失败')
    if request.method!='POST':
        form = LoginForm()#空表单
    else:
        form=LoginForm(request.POST)#获取之后存到了一个cleaned_data字典中
        if form.is_valid():
            username=form.cleaned_data['username']
            password= form.cleaned_data['password']
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                #跳转
                #return redirect('/admin')
                return redirect('users:user_profile')
                #return HttpResponse('success login')
            else:
                # 验证不通过提示！
                return HttpResponse("账号或者密码错误！")
    context={'form':form}

    return render(request, 'users/login.html',context)

def register(request):
    #注册视图
    if request.method!='POST':
        form=RegisterForm()
    else:
        form=RegisterForm(request.POST)
        if form.is_valid():
            new_user=form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.username=form.cleaned_data.get('email')#注注册的时候把email赋值给新用户的username，username和email一样了

            new_user.save()
            send_register_email(form.cleaned_data.get('email'),'register')
            return redirect('users:login')#注册完成转到登录页面
    context={'form':form}
    return render(request, 'users/register.html',context)

class MyBackend(ModelBackend): #email register login
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user=User.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

def active_user(request,active_code):
    #查询验证码 修改用户状态
    all_records=EmailVerifyRecord.objects.filter(code=active_code)
    if all_records:
        for record in all_records:
            email=record.email #得到邮箱
            print(email)
            user=User.objects.get(email=email)  #获取用户
            print(user)
            user.is_staff=True
            user.save()

    else:
        return HttpResponse('链接有错')
    return redirect('users:login')

def forget_pwd(request):
    '找回密码'
    if request.method=='GET':
        form=ForgetPwdForm()#空表单
    elif request.method=='POST':
        form=ForgetPwdForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data.get('email')
            exists=User.objects.filter(email=email).exists()
            if exists:
                #发送邮件
                send_register_email(email,'forget')
                return HttpResponse('邮件已发送请查收')
            else:
                return HttpResponse('邮箱未注册 请注册')
    return render(request,'users/forget_pwd.html',{'form':form})

def forget_pwd_url(request,active_code):
    #修改密码
    if request.method!='POST':
        form=ModifyPwdForm()
    else:
        form=ModifyPwdForm(request.POST)
        if form.is_valid():
            record=EmailVerifyRecord.objects.get(code=active_code)
            email=record.email
            user=User.objects.get(email=email)
            user.username=email
            user.password = make_password(form.cleaned_data.get('password'))
            user.save()
            return HttpResponse('修改成功')
        else:
            return HttpResponse('修改失败')

    return render(request, 'users/reset_pwd.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('users:login')

@login_required(login_url='users:login')   # 设置登录后才能访问，如果没有登陆，就跳转到login界面
def editor_users(request):
    #编辑用户信息
    user=User.objects.get(id=request.user.id)
    if request.method=='POST':
        try:
            #user和userprofile之间是一对一的关系，默认注册的时候是没有数据的，注册成功之后才会在个人中心显示信息
            #第一次登录应该是空表单，如果设置了信息，以后编辑的话就是修改，应该要默认显示原有数据
            userprofile=user.userprofile #模型名称的小写直接拿到用户数据
            form= UserForm(request.POST, instance=user)#instance=user默认显示原有的数据
            print(form)
            user_profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)  # 向表单填充默认数据
            print(user_profile_form)
            if form.is_valid() and user_profile_form.is_valid():
                form.save()
                user_profile_form.save()
                return redirect('users:user_profile')
        except UserProfile.DoesNotExist:  # 这里发生错误说明userprofile无数据
            form = UserForm(request.POST, instance=user)  # 填充默认数据 当前用户 如果userprofile不存在的话 代入user的值
            user_profile_form = UserProfileForm(request.POST, request.FILES)  # 空表单，直接获取空表单的数据保存
            if form.is_valid() and user_profile_form.is_valid():
                form.save()
                # commit=False 先不保存，先把数据放在内存中，然后再重新给指定的字段赋值添加进去，提交保存新的数据
                new_user_profile = user_profile_form.save(commit=False)
                new_user_profile.owner = request.user  #把提交的user（修改的用户名）赋值给models中的owner属性
                new_user_profile.save()
                return redirect('users:user_profile')
    else:
        try:
            userprofile = user.userprofile
            form = UserForm(instance=user)
            user_profile_form = UserProfileForm(instance=userprofile)
        except UserProfile.DoesNotExist:
            form = UserForm(instance=user)
            user_profile_form = UserProfileForm()  # 显示空表单
    return render(request, 'users/editor_users.html', locals())
