from django.db import models
from post.models import PostUserModel
from shared.models import BaseModel
from users.models import UserModel
class LikePostModel(BaseModel):
    post = models.ForeignKey(PostUserModel, on_delete=models.CASCADE, related_name='like')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.post
    
    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'

