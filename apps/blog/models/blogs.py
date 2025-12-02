from django.db import models
from django.utils.text import slugify
from apps.users.models.user_auth import BaseModel
from django.contrib.auth import get_user_model

User = get_user_model()

class BlogCategory(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    
class BlogPost(BaseModel):
    STATUS_CHOICES = (
        (True, "Published"),
        (False, "Draft")
    )
    
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='blogs/images/', null=True, blank=True)
    is_published = models.BooleanField(choices=STATUS_CHOICES, default=False)

    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"
        ordering = ['-created_at']
        
        

