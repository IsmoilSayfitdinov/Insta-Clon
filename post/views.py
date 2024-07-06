from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from post.serializers import PostSerializer
from post.models import PostUserModel
from shared.pagination import CustomPagination
from rest_framework.response import Response
from shared.permissions import IsOwner
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
        
        
        
class PostUpdateViewApi(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = PostSerializer
    
    def put(self, request, pk):
        post = PostUserModel.objects.filter(pk=pk)
        if not post.exists():
            return Response({"message": "not found"})
        
        serializer = PostSerializer(post.first(), data=request.data)
        if serializer.is_valid():
            self.check_object_permissions(obj=post.first(), request=request)
            serializer.save()
            res = {
                "sucsess": True,
                "message": "updated"
            }
            return Response(res)
        else:
            return Response(serializer.errors)
        
        
class DelatePostView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = PostSerializer
    
    def delete(self, request, pk):
        post = PostUserModel.objects.filter(pk=pk)
        if not post.exists():
            return Response({"message": "not found"})
        
        self.check_object_permissions(obj=post.first(), request=request)
        post.delete()
        res = {
            "sucsess": True,
            "message": "deleted"
        }
        return Response(res)
    
    
class UserPostViewApi(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    
    def get_queryset(self):
        return PostUserModel.objects.filter(user=self.request.user)