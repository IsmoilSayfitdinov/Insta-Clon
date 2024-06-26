from django.db import models
from post.models import PostUserModel


class CommnentModel(models.Model):
    post = models.ForeignKey(PostUserModel, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return self.comment
    
    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'



