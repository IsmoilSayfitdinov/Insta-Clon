from django.db import models
from shared.models import BaseModel
from users.models import UserModel
class StoryModel(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='stories')
    media = models.ImageField(upload_to='story_media')
    caption = models.TextField(null=True, blank=True)
    expiry_time = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f"{self.user.username} - {self.caption}"
    
    class Meta:
        ordering = ['-expiry_time']
        verbose_name = 'Story'
        verbose_name_plural = 'Stories'
    
    
class StoryView(BaseModel):
    story = models.ForeignKey(StoryModel, on_delete=models.CASCADE, related_name='story_id')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"{self.user.username} - {self.story.caption}"
    
    
    class Meta:
        ordering = ['-id']
        verbose_name = 'StoryView' 
        verbose_name_plural = 'StoryViews'
    

        
class StoryReactions(BaseModel):
        
    REACTION_CHOICE = [
        ('like', 'Like'),
        ('love', 'Love'),
        ('haha', 'Haha'),
        ('wow', 'Wow'),
        ('sad', 'Sad'),
        ('angry', 'Angry'),
        ('heart', 'Heart'),
    ]    

    reactions = models.CharField(max_length=255, choices=REACTION_CHOICE)
    story = models.ForeignKey(StoryModel, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"{self.user.username} - {self.reactions}"
    
    class Meta:
        ordering = ['-id']
        verbose_name = 'StoryReactions'
        verbose_name_plural = 'StoryReactions'
        
class StoryReport(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    story = models.ForeignKey(StoryModel, on_delete=models.CASCADE)
    reason = models.TextField()
    
    def __str__(self) -> str:
        return f"{self.user.username} - {self.story.caption}"
    
    class Meta:
        ordering = ['-id']
        verbose_name = 'StoryReport'
        verbose_name_plural = 'StoryReports'