from django.db import models
from django.utils import timezone
from blog.models import Post

# Create your models here.
class Comment(models.Model):
    name = models.CharField(max_length=50, verbose_name='姓名')
    email = models.EmailField(verbose_name='邮箱')
    url = models.URLField(blank=True, verbose_name='网址')
    text = models.TextField(verbose_name='评论内容')
    created_time = models.DateTimeField(default = timezone.now(), verbose_name='创建时间')
    post = models.ForeignKey(Post, on_delete = models.CASCADE, verbose_name='文章')

    class Meta:
        db_table = 'comment'
        verbose_name = '评论'
        verbose_name_plural = '评论'
        ordering = ['-created_time']

    def __str__(self):
        return '{}:{}'.format(self.name,self.text[:20])