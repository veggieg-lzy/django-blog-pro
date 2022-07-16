from django.contrib import admin

# Register your models here.
from .models import Category, Post, Tag

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Tag)

#在admin注册以后，admin页面中就会有blog这一个app part 然后下面子分区有博客分类 文章 文章标签三部分
from .models import SideBar
admin.site.register(SideBar)