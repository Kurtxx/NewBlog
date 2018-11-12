from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify

# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=140)
    subcategory = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='subcategory_category_fk', null=True, blank=True)
    slug = models.SlugField(max_length=140, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('post-create') #Przechodzi do dodawania posta (Dodał Kategorię)


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='post_category_fk', null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk':self.pk})



class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
