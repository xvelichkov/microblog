from django import forms
from .models import Comment, Post


class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['body', 'image']


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
