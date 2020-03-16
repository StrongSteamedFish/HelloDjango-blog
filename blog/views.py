from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post, Category, Tag
# 导入markdown模块
import markdown
# 导入正则匹配模块
import re
# 导入slugify和TocExtension模块
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension


# Create your views here.

# 主页视图
def index(request):
    # 获取Post全部信息列表[Post.objects.all()]，(并倒序排序[order_by('created_time')]已经在Post类内实现了)
    post_list = Post.objects.all()
    # 将排序好的post_list作为参数传给模板index.html
    return render(request,'blog/index.html',context={'post_list':post_list})

# 详情页视图
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # 实例化一个Markdown对象
    md = markdown.Markdown(extensions=[
        # 引入扩展
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        # 将字符串扩展'markdown.extensions.toc'换成一个TocExtension实例
        # 该实例在实例化时可以传入一个slugify参数，这个参数的类型是一个函数
        # markdown将使用这个函数来替代内置的处理标题用的函数
        # 这里调用的是django的一个工具类中的函数slugify来更好的处理中文
        TocExtension(slugify=slugify)
    ])
    # 该对象的调用convert方法对body的内容转化格式，并返回转化后的html文档格式
    post.body = md.convert(post.body)
    # 调用convert格式后的md会生成toc（目录）值，调用目录值可以获得目录的html文档
    # 用正则表达式匹配md中的目录文档，查看ul中是否有值
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    # 如果有值则把ul中的值返回给toc，如果没有则返回空字符串（用于html中检测判断）
    post.toc = m.group(1) if m is not None else ''
    return render(request, 'blog/detail.html', context={'post':post})

# 归档页视图
def archive(request, year, month):
    # 根据归档的年月筛选文章
    post_list = Post.objects.filter(
        created_time__year = year,
        created_time__month = month
    )
    # # 将文章通过创建时间倒序排列
    # post_list = post_list.order_by('-created_time')
    # 因为详情页和首页展示完全一样，所以直接复用了首页index.html的模板（但是显示的请求url地址还是archive，只是借助了其模板）
    return render(request, 'blog/index.html', context={'post_list':post_list})

# 分类页视图
def category(request, pk):
    cate = get_object_or_404(Category, pk = pk)
    post_list = Post.objects.filter(category = cate)
    # post_list = post_list.order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list':post_list})

# 标签页视图
def tag(request, pk):
    t = get_object_or_404(Tag, pk = pk)
    post_list = Post.objects.filter(tag = t)
    # post_list = post_list.order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list':post_list})