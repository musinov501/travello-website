from rest_framework import generics, permissions, status
from rest_framework.response import Response

from apps.blog.serializers.blog_serializer import (
    BlogCategorySerializer,
    BlogPostSerializer
)
from apps.blog.models.blogs import BlogPost, BlogCategory


class BlogListView(generics.ListAPIView):
    """
    List all published blog posts.
    """
    queryset = BlogPost.objects.filter(is_published=True)
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        posts = self.get_queryset()
        serializer = self.get_serializer(posts, many=True)

        return Response({
            "status": "success",
            "count": posts.count(),
            "message": "Blog posts retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class BlogDetailView(generics.RetrieveAPIView):
    """
    Retrieve a single blog post by slug.
    """
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.AllowAny]

    lookup_field = "slug"
    lookup_url_kwarg = "slug"

    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()
        serializer = self.get_serializer(post)

        return Response({
            "status": "success",
            "message": "Blog post retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class BlogCreateView(generics.CreateAPIView):
    """
    Create a new blog post (Admin only).
    """
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        post = serializer.save(author=request.user)

        return Response({
            "status": "success",
            "message": "Blog post created successfully",
            "data": BlogPostSerializer(post).data
        }, status=status.HTTP_201_CREATED)


class BlogUpdateView(generics.UpdateAPIView):
    """
    Update an existing blog post (Admin only).
    """
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAdminUser]

    lookup_field = "slug"
    lookup_url_kwarg = "slug"

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        post = serializer.save()

        return Response({
            "status": "success",
            "message": "Blog post updated successfully",
            "data": BlogPostSerializer(post).data
        }, status=status.HTTP_200_OK)


class BlogDeleteView(generics.DestroyAPIView):
    """
    Delete a blog post by slug (Admin only).
    """
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAdminUser]

    lookup_field = "slug"
    lookup_url_kwarg = "slug"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        deleted_slug = instance.slug
        instance.delete()

        return Response({
            "status": "success",
            "message": "Blog post deleted successfully",
            "data": {
                "slug": deleted_slug
            }
        }, status=status.HTTP_200_OK)
