from django.db import models
from post.models import PostUserModel
from users.models import UserModel
from shared.models import BaseModel
class CommnentModel(BaseModel):
    post = models.ForeignKey(PostUserModel, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    comment = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name="children", null=True, blank=True)

    def __str__(self):
        return self.comment
    
    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'



class CommentLikeModel(BaseModel):
    comment = models.ForeignKey(CommnentModel, on_delete=models.CASCADE, related_name='like')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.comment.comment
    
    class Meta:
        verbose_name = 'LikeComment'
        verbose_name_plural = 'LikesComent'