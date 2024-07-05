from users.models import UserModel
from shared.models import BaseModel
from django.db import models
# Create your models here.
class PostUserModel(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE , related_name='posts')
    image = models.ImageField(upload_to='post_image')
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    tags = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title
    
    
    class Meta: 
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'