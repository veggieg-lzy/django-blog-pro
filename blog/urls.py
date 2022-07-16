from django.urls import path
from . import views

app_name = 'blog'   # 定义一个命名空间，用来区分不同应用之间的链接地址
urlpatterns = [
    path('', views.index, name='index'),#url的名字，方法，命名空间
    path('category/<int:categoty_id>/', views.category_list, name='category_list'),
    path('detail/<int:post_id>/',views.post_detail,name='post_detail'),
    path('search/',views.search,name='search')

]