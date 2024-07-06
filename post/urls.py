from django.urls import path
from comment.views import ComenntViewList, CreateCommnet, CommnetLikeView, CommentUpdateViewApi, DelateCommnetView
from .views import PostView, PostCreateView, PostUpdateViewApi, DelatePostView, UserPostViewApi
from like.views import MyLikeUserView
from like.views import LikePostView
urlpatterns = [
   path('', PostView.as_view()),
   path('create/', PostCreateView.as_view()),
   path('<int:pk>/update/', PostUpdateViewApi.as_view()),
   path('<int:pk>/delete/', DelatePostView.as_view()),
   path('<int:pk>/like/', LikePostView.as_view()),
   path('myposts/', UserPostViewApi.as_view()),
   
   path('<int:pk>/comments/', ComenntViewList.as_view()),
   path('<int:pk>/comments/create/', CreateCommnet.as_view()),
   path('comments//<int:pk>/like/', CommnetLikeView.as_view()),
   path('comments/<int:pk>/update/', CommentUpdateViewApi.as_view()),
   path('comments/<int:pk>/delete/', DelateCommnetView.as_view()),
   
   
   path('mylikes/', MyLikeUserView.as_view()),
   
]