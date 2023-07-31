from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from users.models import User
# Create your models here.    
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    view_count = models.PositiveIntegerField(default=0)
    file = models.FileField(upload_to='post_files/')
    language = models.CharField(max_length=10)
    
    def __str__(self):
        return self.title
    
    def get_filename(self):
        return os.path.basename(self.file.name)
    
class Reply(models.Model):
    contents = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-id']