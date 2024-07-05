from django.urls import path
from comment.views import ComenntViewList, CreateCommnet
from .views import PostView, PostCreateView
urlpatterns = [
   path('', PostView.as_view()),
   path('create/', PostCreateView.as_view()),
   path('<int:pk>/comments/', ComenntViewList.as_view()),
   path('<int:pk>/comments/create/', CreateCommnet.as_view()),
]