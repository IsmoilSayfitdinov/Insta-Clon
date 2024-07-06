from rest_framework import serializers
from .models import LikePostModel

class LikeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = LikePostModel
        fields = '__all__'