from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from comment.models import CommnentModel
from shared.pagination import CustomPagination
from comment.serializers import CommentSerializer
from post.models import PostUserModel
# Create your views here.
class ComenntViewList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        post_id = self.kwargs.get("pk")
        return CommnentModel.objects.filter(post_id = post_id)
    
    
class CreateCommnet(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        post_id = self.kwargs.get("pk")
        serializer.save(user = self.request.user, post_id = post_id)
    