from rest_framework import serializers
from comment.models import CommnentModel
from post.serializers import UserSerializer

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    me_liked = serializers.SerializerMethodField('get_me_liked')
    replies = serializers.SerializerMethodField('get_replies')

    class Meta:
        model = CommnentModel
        fields = ['id', 'uuid', 'comment', 'me_liked', 'user', 'replies']

    def get_me_liked(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.like.filter(user=user).exists()
        return False

    def get_replies(self, obj):
        serializer = self.__class__(obj.children.all(), many=True, context=self.context)
        return serializer.data