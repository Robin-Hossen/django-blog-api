from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
# custom user model
class User(AbstractUser):
    def __str__(self):
        return self.username



class AuthorProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    bio=models.TextField(blank=True)
    website=models.URLField(blank=True)
    profile_picture=models.ImageField(upload_to='profile_pictures/',blank=True,null=True)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name=models.CharField(max_length=100,unique=True)
    slug=models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name=models.CharField(max_length=100,unique=True)
    slug=models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title=models.CharField(max_length=200)
    slug=models.SlugField(unique=True)
    content=models.TextField()
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name="posts")
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,related_name="posts")
    tags=models.ManyToManyField(Tag,related_name="posts",blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    likes=models.ManyToManyField(User,related_name="liked_posts",blank=True)
    views_count=models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Bookmark(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="bookmarks")
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="bookmarked_by")
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post') #ak jon user ekta post ke multiple bar bookmark korte parbe na

    def __str__(self):
        return f"{self.user.username} bookmarked {self.post.title}"

class NewsletterSubscription(models.Model):
    email=models.EmailField(unique=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email        

class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="comments")
    body=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"