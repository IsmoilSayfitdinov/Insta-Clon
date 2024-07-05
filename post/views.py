from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from post.serializers import PostSerializer
from post.models import PostUserModel
from shared.pagination import CustomPagination

class PostView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination
    def get_queryset(self):
        return PostUserModel.objects.all()
    
    
class PostCreateView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)