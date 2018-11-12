from django import forms
from django.db import models
from django.contrib.auth.models import User
from .models import Post, Comment

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']
