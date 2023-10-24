from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    followers = models.ManyToManyField('self', related_name='followed_by', blank=True, symmetrical=False)
    following = models.ManyToManyField('self', related_name='follows', blank=True, symmetrical=False)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/user.png')
    
    def __str__(self):
        return self.username
    
class CommentModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    post = models.ForeignKey('PostModel', on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.user} on Post {self.post.id}: {self.text[:50]}"  

class PostModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')
    body = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now=True)
    comments = models.ManyToManyField(CommentModel, related_name='comments_on_post', blank=True)
  
    def __str__(self):
        return f"Post by {self.author}: {self.body[:50]}"  # Zwraca pierwsze 50 znaków treści posta.

class LikeModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='post_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Like by {self.user} on Post {self.post.id}"

