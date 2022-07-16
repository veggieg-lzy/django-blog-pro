from django import template
from blog.models import Category,Post,SideBar
#把一些方法注册成tag，可以直接在html模板中调用 调用时候不用加（）

#自定义模板标签  是template.Library类
register = template.Library()  #注册

@register.simple_tag
def get_category_list():
    #获取分类的列表
    return Category.objects.all()

@register.simple_tag
def get_post_list():
    #获取分类的列表
    return Post.objects.all()


@register.simple_tag
def get_sidebar_list():
    return SideBar.get_sidebar()

@register.simple_tag
def get_new_post():
    #获取最新文章
    return Post.objects.order_by('-pub_date')[:8]