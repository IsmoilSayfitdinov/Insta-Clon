from django.urls import path
from comment.views import ComenntViewList, CreateCommnet, CommnetLikeView
from .views import PostView, PostCreateView
from like.views import LikePostView
urlpatterns = [
   path('', PostView.as_view()),
   path('create/', PostCreateView.as_view()),
   path('<int:pk>/comments/', ComenntViewList.as_view()),
   path('<int:pk>/comments/create/', CreateCommnet.as_view()),
   path('<int:pk>/like/', LikePostView.as_view()),
   path('<int:pk>/comments/like/', CommnetLikeView.as_view()),
]