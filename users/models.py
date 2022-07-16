from django.db import models
# 首先引入django内置的一个用户User模型，然后通过一对一关联关系为默认的User扩展用户数据
from django.contrib.auth.models import User
# Create your models here.

#扩展用户模型的方法有两种，一种是模仿官方的方法，直接继承`AbstractUser`类来扩展用户数据，另外一种是通过一对一关系关联User类，来扩展用户数据，我这里选择采用第二种一对一关联的方式来扩展，这样的好处是不需要再setiings.py中另外配置，也有利于我们理解和学习django的关联关系用法。
#我们为默认的User扩展数据便是使用一对一关系即OneToOneField，字段来相互关联扩展，一个用户只能对应唯一的一组数据，因此上这里就必须使用一对一关系关联。

class UserProfile(models.Model):
    USER_GENDER_TYPE = (
        ('male', '男'),
        ('female', '女'),
    )
    owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    nike_name = models.CharField('昵称', max_length=50, blank=True, default='')#提交表单时，允许这一项为空
    birthday = models.DateField('生日', null=True, blank=True)
    gender = models.CharField('性别', max_length=6, choices=USER_GENDER_TYPE, default='male')
    address = models.CharField('地址', max_length=100, blank=True, default='')
    image = models.ImageField(upload_to='images/%Y/%m', default='images/default.png', max_length=100,
                              verbose_name='用户头像')

    desc=models.TextField('个人简历',max_length=200,blank=True,default='') #可以为空 一开始不设置
    gexing = models.CharField('个性签名', max_length=100, blank=True, default='')

    class Meta:
        verbose_name = '用户数据'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.owner.username

class EmailVerifyRecord(models.Model):#邮箱验证码校验记录
    SEND_TYPE_CHOICES = (
        ('register', '注册'),
        ('forget', '找回密码'),
    )
    code=models.CharField('验证码',max_length=30)
    email=models.CharField('邮箱',max_length=50)
    send_type = models.CharField(choices=SEND_TYPE_CHOICES, max_length=10, default='register')
    send_time = models.DateTimeField('时间', auto_now_add=True)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code


