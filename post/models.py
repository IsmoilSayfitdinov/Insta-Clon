from django.db import models
from users.models import UserModel


# Create your models here.
class PostUserModel(models.Model):
    users = models.ManyToManyField(UserModel)
    image = models.ImageField(upload_to='post_image')
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    tags = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title
    
    
    class Meta: 
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'