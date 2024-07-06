from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from comment.models import CommnentModel
from shared.pagination import CustomPagination
from comment.serializers import CommentSerializer
from post.models import PostUserModel
from comment.models import CommentLikeModel
from rest_framework.views import APIView
from rest_framework.response import Response
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
    
    
class CommnetLikeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        comment_like = CommentLikeModel.objects.filter(comment_id = pk, user = request.user)
        
        if comment_like.exists():
            comment_like.delete()
            res = {
                "sucsess": True,
                "message": "unliked"
            }
            return Response(res)
        else:
            CommentLikeModel.objects.create(comment_id = pk, user = request.user)
            res = {
                "sucsess": True,
                "message": "liked"
            }
            return Response(res)