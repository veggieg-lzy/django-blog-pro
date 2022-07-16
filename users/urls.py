from django.urls import path
from . import views

app_name = 'users'   # 定义一个命名空间，用来区分不同应用之间的链接地址
urlpatterns = [
    path(r'login.html', views.login_view, name='login'),#url的名字，方法，空间命名
    path(r'register.html', views.register, name='register'),
    path(r'active/<active_code>',views.active_user,name='active_user'),
    path(r'forget_pwd.html',views.forget_pwd,name='forget_pwd'),
    path(r'forget_pwd_url/<active_code>',views.forget_pwd_url,name='reset_pwd'),
    path(r'user_profile.html',views.user_profile,name='user_profile'),
    path(r'logout/',views.logout_view,name='logout1'),
    path(r'editor_users/',views.editor_users,name='editor_users'),
]
#r'^login/'