from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    UserPostListView,
    AddComment,
    KategoriaCreateView,
    CategoryDetail,
)

from . import views


urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),

    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),

    # np /blog/<post_id>/ (ID = PK)
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),

    # np /blog/new/
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),

    # np /blog/2/update/
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),

    # np /blog/2/delete/
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),

    # np /blog/2/comment/
    path('post/<int:pk>/comment/', views.AddComment, name='add-comment'),

    # np /blog/nowakategoria
    path('category/add/', views.KategoriaCreateView.as_view(), name='category-create'),

    # path('category/<str:slug>/', views.CategoryDetail.as_view(), name='category-detail'),
    path('category/<str:slug>/', CategoryDetail, name='category-detail'),

    path('about/', views.about, name='blog-about'),
]
