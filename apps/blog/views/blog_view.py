from apps.blog.serializers.blog_serializer import (
    BlogCategorySerializer,
    BlogPostSerializer
)
from rest_framework import generics, permissions
from apps.blog.models.blogs import BlogPost, BlogCategory


class BlogListView(generics.ListAPIView):
    queryset = BlogPost.objects.filter(is_published=True)
    serializer_class = BlogPostSerializer
    
class BlogDetailView(generics.RetrieveAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    
    lookup_field = "slug"
    lookup_url_kwarg = "slug"


class BlogCreateView(generics.CreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class BlogUpdateView(generics.UpdateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAdminUser]
    
    lookup_field = "slug"
    lookup_url_kwarg = "slug"


class BlogDeleteView(generics.DestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAdminUser]
    
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
    



