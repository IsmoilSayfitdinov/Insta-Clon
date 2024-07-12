from rest_framework import serializers
from .models import StoryModel, StoryView, StoryReactions, StoryReport
from post.serializers import UserSerializer

class StoryUpdateSerializers(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    expiry_time = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = StoryModel
        fields = "__all__"
        
        
class StoryViewSerializers(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = StoryView
        fields = "__all__"
        
        
class StoryReactionsSerializers(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = StoryReactions
        fields = "__all__"
        

class StoryReportSerializers(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = StoryReport
        fields = "__all__"
        
        