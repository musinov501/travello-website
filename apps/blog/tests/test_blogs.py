from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

from apps.blog.models.blogs import BlogPost

User = get_user_model()


class BlogAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        # Create admin user
        self.admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin123"
        )

        # Create normal user
        self.normal_user = User.objects.create_user(
            username="user",
            email="user@example.com",
            password="user123"
        )

        # Create blog post
        self.blog = BlogPost.objects.create(
            title="Test Blog",
            slug="test-blog",
            content="Content here",
            author=self.admin_user,
            is_published=True
        )

        # URLs
        self.list_url = reverse("blog:blog-list")
        self.create_url = reverse("blog:blog-create")
        self.detail_url = reverse("blog:blog-detail", kwargs={"slug": self.blog.slug})
        self.update_url = reverse("blog:blog-update", kwargs={"slug": self.blog.slug})
        self.delete_url = reverse("blog:blog-delete", kwargs={"slug": self.blog.slug})

    # ----------------------------------------------------
    # LIST
    # ----------------------------------------------------
    def test_blog_list(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["slug"], "test-blog")

    # ----------------------------------------------------
    # DETAIL
    # ----------------------------------------------------
    def test_blog_detail(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Blog")

    # ----------------------------------------------------
    # CREATE (Admin only)
    # ----------------------------------------------------
    def test_blog_create_admin(self):
        self.client.force_authenticate(user=self.admin_user)

        data = {
            "title": "New Blog",
            "slug": "new-blog",
            "content": "New content",
            "is_published": True
        }

        response = self.client.post(self.create_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(BlogPost.objects.filter(slug="new-blog").exists())

    def test_blog_create_forbidden_for_user(self):
        self.client.force_authenticate(user=self.normal_user)

        data = {
            "title": "User Blog",
            "slug": "user-blog",
            "content": "Unauth content"
        }

        response = self.client.post(self.create_url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ----------------------------------------------------
    # UPDATE
    # ----------------------------------------------------
    def test_blog_update_admin(self):
        self.client.force_authenticate(user=self.admin_user)

        data = {
            "title": "Updated Title",
            "content": "Updated content",
            "is_published": True
        }

        response = self.client.put(self.update_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.blog.refresh_from_db()
        self.assertEqual(self.blog.title, "Updated Title")

    # ----------------------------------------------------
    # DELETE
    # ----------------------------------------------------
    def test_blog_delete_admin(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.delete(self.delete_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(BlogPost.objects.filter(slug="test-blog").exists())
