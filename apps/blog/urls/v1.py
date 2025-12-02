from django.urls import path
from apps.blog.views.blog_view import (
    BlogCreateView,
    BlogDetailView,
    BlogDeleteView,
    BlogListView,
    BlogUpdateView
)

app_name = 'blog'

urlpatterns = [
    path('', BlogListView.as_view(), name='blog-list'),
    path('create/', BlogCreateView.as_view(), name='blog-create'),
    path('<slug:slug>/', BlogDetailView.as_view(), name='blog-detail'),
    path('<slug:slug>/update/', BlogUpdateView.as_view(), name='blog-update'),
    path('<slug:slug>/delete/', BlogDeleteView.as_view(), name='blog-delete'),
]




