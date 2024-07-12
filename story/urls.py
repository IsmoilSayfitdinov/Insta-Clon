from django.urls import path
from .views import  StoryCreateView, StoryViewApi, StoryReactionsViewApi, UserStoryView, StoryDelete, StoryViewList, StoryReportViewApi
urlpatterns = [
    path('create/', StoryCreateView.as_view()),
    path('view/', StoryViewApi.as_view()),
    path('view/<int:story_id>/', StoryViewList.as_view()),
    path('user/', UserStoryView.as_view()),
    path('reactions/', StoryReactionsViewApi.as_view()),
    path('delete/<int:pk>/', StoryDelete.as_view()),
    path('report/', StoryReportViewApi.as_view()),
]   