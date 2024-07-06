from rest_framework import serializers
from .models import PostUserModel
from users.models import UserModel
from like.models import LikePostModel
from comment.models import CommnentModel
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserModel
        fields = ['uuid', 'avatar', 'username']
        

class PostSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField("get_like_count")
    comment_count = serializers.SerializerMethodField("get_comment_count")
    user = UserSerializer(read_only=True)
    me_like = serializers.SerializerMethodField("get_me_like")
    
    class Meta:
        model = PostUserModel
        fields = ["id", "uuid", "image", "title", "description", "like_count", "user", "me_like", "comment_count"]
        
    @staticmethod
    def get_like_count(obj):
        return 0
    
    @staticmethod
    def get_comment_count(obj):
        return obj.comments.count()   
    
    def get_me_like(self, obj):
        request = self.context.get('request', None)
        return LikePostModel.objects.filter(post=obj, user=request.user).exists()



