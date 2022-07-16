#之前是通过html定义表单并获取表单数据 现在通过forms.py来构建表单
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile



class LoginForm(forms.Form):
    username=forms.CharField(label='用户名',max_length=30,widget=forms.TextInput(attrs={
        'class':'input','placeholder':'用户名/邮箱'
    })) #网页中显示的输入框
    #使用widget参数来设置样式
    #最后一个参数让输入的密码不显示
    password = forms.CharField(label='密码', min_length=6, widget=forms.PasswordInput(attrs={
        'class':'input','placeholder':'密码'
    }))
    def clean_password(self):
        username=self.cleaned_data.get('username')
        password=self.cleaned_data.get('password')
        if username==password:
            raise forms.ValidationError('密码用户名相同')
        return password

class RegisterForm(forms.ModelForm):
#class RegisterForm(LoginForm,forms.ModelForm):#通过继承上面的登录表单和ModelForm(主要是里面的save方法，在views.py中用到了)
    # username=forms.CharField(label='用户名',max_length=30,widget=forms.TextInput(attrs={
    #     'class': 'input', 'placeholder': '用户名/邮箱'
    # }))#前一个用户名在网页中是那个实体字label 后面一个用户名/邮箱在页面中是框框中的浅色字体
    email=forms.EmailField(label='邮箱',max_length=30,widget=forms.EmailInput(attrs={
            'class': 'input', 'placeholder': '邮箱'
        }))
    password=forms.CharField(label='密码',min_length=6,widget=forms.PasswordInput(attrs={
        'class': 'input',
        'placeholder': '密码'
    }))
    password1=forms.CharField(label='再次密码',min_length=6,widget=forms.PasswordInput(attrs={
        'class':'input',
        'placeholder':'再次密码'
    }))
    class Meta:
        model=User
        fields = ('email', 'password')
        #fields=('username','password')#注册页面中需要的属性就选出来放在这里
    def clean_email(self):
        email=self.cleaned_data.get('email')
        exists=User.objects.filter(email=email).exists()
        if exists:
            raise forms.ValidationError('邮箱已存在')
        return email
    def clean_username(self):
        username=self.cleaned_data.get('username')
        exists=User.objects.filter(username=username).exists()
        if exists:
            raise forms.ValidationError('用户名已存在')
        return username
    #验证两次密码是否一样
    def clean_password1(self):
        data=self.cleaned_data
        password=data['password']
        password1=data['password1']
        if password!=password1:
            raise forms.ValidationError('密码不一致')
        return password

#找回密码表单
class ForgetPwdForm(forms.Form):
    email=forms.EmailField(label='请输入邮箱地址',min_length=4, widget=forms.EmailInput(attrs={
        'class': 'input', 'placeholder': '用户名/邮箱'
    }))

#修改密码表单
class ModifyPwdForm(forms.Form):
    password=forms.CharField(label='输入新密码',min_length=6,widget=forms.PasswordInput(attrs={
        'class':'input',
        'placeholder':'输入新密码'
    }))

#修改用户信息的表单
class UserForm(forms.ModelForm):
    """ User模型的表单，只允许修改email一个数据，用户名不允许修改 """
    #邮箱信息是可以修改的
    class Meta:
        model = User
        fields = ('email',)
class UserProfileForm(forms.ModelForm):
    """ UserProfile的表单 """
    class Meta:
        """Meta definition for UserInfoform."""
        model = UserProfile
        fields = ('nike_name','desc', 'gexing', 'birthday',  'gender', 'address', 'image')