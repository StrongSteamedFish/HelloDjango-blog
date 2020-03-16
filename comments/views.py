from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from .forms import CommentForm
from blog.models import Post
from django.contrib import messages

# Create your views here.
@require_POST
def comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    # 通过request提交的表单数据构建Form对象（具体实现是CommentForm类）
    form = CommentForm(request.POST)

    # is_valid()自动检测提交的表单内容是否符合格式
    if form.is_valid():
        # 数据合法

        # 保存生成实例，但不保存到数据库（commit = False）
        # 由于form是CommentForm类的实例，所以这里保存生成的实例是一个Comment表数据实例
        comment = form.save(commit = False)
        # 储存被评论的文章信息
        comment.post = post
        # 保存到数据库
        comment.save()
        # 发送[成功]消息到浏览器的缓存中
        messages.add_message(request, messages.SUCCESS, '评论发表成功！', extra_tags='success')
        # 重定向到这条post的首页（也就是没有离开此界面，因为该请求是从此页面发出的）
        # 这里redirect函数接受到一个表数据模型的实例时，是调用它的get_absolute_url方法
        # （django内部规定的，用户在表中需要自己定义这个方法）
        return redirect(post)
    # 数据不合法

    # 发送[失败]消息到浏览器的缓存中
    messages.add_message(request, messages.ERROR, '评论发表失败！请修改表单中的错误后重新提交。', extra_tags='danger')
    # 返回一个包含错误提示的页面：
    context = {
        'post':post,
        'form':form
    }
    return render(request, 'comments/preview.html', context = context)

# test