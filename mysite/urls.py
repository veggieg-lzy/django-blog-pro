"""mysite URL Configuration
#django项目的url声明 可以理解为网站的“目录”
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
#静态文件配置
urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),#第一个参数可以改成任意值 在网页中输入相应的值即可
    path('',include('blog.urls'))
]+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

#媒体文件配置
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)