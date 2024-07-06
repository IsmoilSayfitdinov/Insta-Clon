from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from like.models import LikePostModel
from rest_framework.response import Response
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