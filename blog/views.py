from django.db.models import Q
from django.shortcuts import render, get_object_or_404

# Create your views here.
from blog.models import Category,Post,Tag
#django自带的分页方法
from django.core.paginator import Paginator

def index(request):
    #首页
    #category_list=Category.objects.all()
    post_list=Post.objects.all()
    paginator = Paginator(post_list, 2)  # 第二个参数2代表每页显示几个
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'post_list': post_list, 'page_obj': page_obj}
    #context={'category_list':category_list,'post_List':post_list}
    return render(request,'blog/index.html',context)

#分类页 进行分页
def category_list(request,categoty_id):
    #分类列表 测试分类1 测试分类2
    category=get_object_or_404(Category,id=categoty_id)
    print(category)
    #获取当前分类下的所有文章 测试分类1的所有文章 测试分类2的所有文章
    posts=category.post_set.all()
    print(posts)
    paginator = Paginator(posts, 2)  # 第二个参数2代表每页显示几个
    page_number = request.GET.get('page')  # http://assas.co/?page=1 (页码)
    page_obj = paginator.get_page(page_number)
    context={'category':category, 'page_obj': page_obj}#前面的参数是空间名 在前端html中要引用的话就要用前面那个参数
    return render(request,'blog/list.html',context)

#文章详情
def post_detail(request,post_id):
    #文章详页
    post=get_object_or_404(Post,id=post_id)
    print(post)
    prev_post=Post.objects.filter(id_lt=post_id).last()
    next_post = Post.objects.filter(id_gt=post_id).first()
    date_prev_post=Post.objects.filter(add_date_lt=post.add_date).last()
    date_next_post=Post.objects.filter(add_date_gt=post.add_date).first()
    context={'post':post,'prev_post':prev_post,'next_post':next_post}
    #print(context)
    return render(request,'blog/detail.html',context)

def search(request):
    #搜索视图
    keyword=request.GET.get('keyword')
    #没有搜索默认显示所有文章
    if not keyword:
        post_list=Post.objects.all()#内部自带查询方法 查询所有的文章
    else:
        post_list=Post.objects.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword) |Q(content__icontains=keyword))

    paginator=Paginator(post_list,2)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)


    context={
        'page_obj':page_obj
    }
    return render(request,'blog/index.html',context)
