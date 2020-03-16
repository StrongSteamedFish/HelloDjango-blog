from django import forms
from .models import Comment

# 创建评论表单
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'url', 'text']