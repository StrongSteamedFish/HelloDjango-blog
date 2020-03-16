from django.db import models
# 导入User类(表)关联文章表
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
# 导入markdown模块
import markdown
# 导入用于去除html标签的工具strip_tags
from django.utils.html import strip_tags

# Create your models here.

# 表-分类
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='分类名')
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'category'
        verbose_name = '分类'
        verbose_name_plural = verbose_name

# 表-标签
class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name='标签名')
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'tag'
        verbose_name = '标签'
        verbose_name_plural = verbose_name
    

# 表-文章
class Post(models.Model):
    # 标题
    title = models.CharField(max_length=70, verbose_name='标题')
    # 正文
    body = models.TextField(verbose_name='正文')
    # 文章摘要
    # 文章可以没有摘要blank=True
    excerpt = models.CharField(max_length=200, blank=True, verbose_name='文章摘要')
    # 创建时间和修改时间
    created_time = models.DateTimeField(verbose_name='创建时间', default=timezone.now())
    modified_time = models.DateTimeField(verbose_name='修改时间')
    # 分类（多对一）使用外键关联分类表
    # models.CASCADE:当关联的分类被删除时，该分类下的全部文章都被删除
    category = models.ForeignKey(Category, on_delete = models.CASCADE, verbose_name='分类')
    # 标签（多对多）使用多对多关联标签表（会自动创建一张关联用表）
    # 允许文章没有标签blank=True
    tag = models.ManyToManyField(Tag, blank=True, verbose_name='标签')
    # 作者
    # 导入了User类(表)用来关联外键，当作者被删除时，该作者的全部文章都被删除
    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name='作者')
    class Meta:
        db_table = 'post'
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return self.title

    # 复写该类的保存方法save()，让每次数据存储时都能更新修改时间
    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()
        # 自动生成文章摘要功能：
        # 实例化一个Markdown对象用于转化body内容
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        # 转化body内容并去除html标签然后返回前52个字符加[……]作为文章的摘要
        self.excerpt = strip_tags(md.convert(self.body))[:52] + '……'
        # 调用父类的save方法保存
        super().save(*args, **kwargs)

    # 为post类创建一个返回自身详情路径的方法
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})