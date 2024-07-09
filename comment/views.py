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
from shared.permissions import IsOwner
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
    
    def get_queryset(self):
        return CommnentModel.objects.all()
    
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
        
class CommentUpdateViewApi(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = CommentSerializer
    
    def put(self, request, pk):
        comment = CommnentModel.objects.filter(pk=pk)
        if not comment.exists():
            return Response({"message": "not found"})
        
        serializer = CommentSerializer(comment.first(), data=request.data)
        if serializer.is_valid():
            self.check_object_permissions(obj=comment.first(), request=request)
            serializer.save()
            res = {
                "sucsess": True,
                "message": "updated"
            }
            return Response(res)
        else:
            return Response(serializer.errors)
        
class DelateCommnetView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = CommentSerializer
    
    def delete(self, request, pk):
        commnet = CommnentModel.objects.filter(pk=pk)
        if not commnet.exists():
            return Response({"message": "not found"})
        
        self.check_object_permissions(obj=commnet.first(), request=request)
        commnet.delete()
        res = {
            "sucsess": True,
            "message": "deleted"
        }
        return Response(res)