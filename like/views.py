from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from like.models import LikePostModel
from rest_framework.response import Response
from rest_framework import generics
from .serializers import LikeSerializer
# Create your views here.
class LikePostView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        post_like = LikePostModel.objects.filter(post_id = pk, user = request.user)
        
        if post_like.exists():
            post_like.delete()
            res = {
                "sucsess": True,
                "message": "unliked"
            }
            return Response(res)
        else:
            LikePostModel.objects.create(post_id = pk, user = request.user)
            res = {
                "sucsess": True,
                "message": "liked"
            }
            return Response(res)
        
class MyLikeUserView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer
    
    def get_queryset(self):
        return LikePostModel.objects.filter(user=self.request.user)