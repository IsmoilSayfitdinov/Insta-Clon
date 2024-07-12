from django.shortcuts import render
from rest_framework import generics
from .serializers import StoryUpdateSerializers, StoryViewSerializers, StoryReactionsSerializers, StoryReportSerializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.utils import timezone
from .models import StoryView, StoryReactions, StoryModel, StoryReport
class StoryCreateView(generics.CreateAPIView):
    serializer_class = StoryUpdateSerializers
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user, expiry_time=timezone.now() + timezone.timedelta(days=1), is_active=True)
            return Response(serializer.data, status=201)
        else: 
            return Response(serializer.errors, status=400)


class StoryViewApi(generics.CreateAPIView):
    serializer_class = StoryViewSerializers
    permission_classes = [IsAuthenticated]
    queryset = StoryModel.objects.all()
    
    def perform_create(self, serializer):
        story_id = self.request.data['story']
        serializer.save(user=self.request.user, story_id=story_id)
        

class UserStoryView(generics.ListAPIView):
    serializer_class = StoryUpdateSerializers
    permission_classes = [IsAuthenticated]
    queryset = StoryModel.objects.all()
    
    def get_queryset(self):
        return StoryModel.objects.filter(user=self.request.user, expiry_time__gt=timezone.now())


class StoryViewList(generics.ListAPIView):
    queryset = StoryView.objects.all()
    serializer_class = StoryViewSerializers
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self , *args, **kwargs):
        return StoryView.objects.filter(story_id = self.kwargs["story_id"])


class StoryReactionsViewApi(generics.CreateAPIView):
    serializer_class = StoryReactionsSerializers
    permission_classes = [IsAuthenticated]
    queryset = StoryReactions.objects.all()
    
    def perform_create(self, serializers):
        story_id = self.request.data['story']
        serializers.save(user=self.request.user, story_id=story_id, reactions=self.request.data['reactions'])

class StoryReportViewApi(generics.CreateAPIView):
    serializer_class = StoryReportSerializers
    permission_classes = [IsAuthenticated]
    queryset = StoryReport.objects.all()
    
    def perform_create(self, serializers):
        story_id = self.request.data['story']
        reason = self.request.data['reason']
        serializers.save(user=self.request.user, story_id=story_id, reason=reason)



class StoryDelete(generics.DestroyAPIView):
    serializer_class = StoryUpdateSerializers
    permission_classes = [IsAuthenticated]
    queryset = StoryModel.objects.all()
    
    def get_queryset(self):
        return StoryModel.objects.filter(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        
        res = {
            "sucsess": True,
            "message": "deleted"
        }
        return Response(res)
        
        
