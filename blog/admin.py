from django.contrib import admin
from .models import Post, Tag, Category

class PostAdmin(admin.ModelAdmin):
    # 控制列表页展示的字段
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']
    # 控制表单展现的字段
    fields = ['title', 'body', 'excerpt', 'category' ,'tag']
    # 复写save_model函数，将请求的用户信息绑定到表单中
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Category)