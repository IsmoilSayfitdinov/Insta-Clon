from django.db import models
from post.models import PostUserModel
class LikePostModel(models.Model):
    post = models.ForeignKey(PostUserModel, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.post
    
    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'

