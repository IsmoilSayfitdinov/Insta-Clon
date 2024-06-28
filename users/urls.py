from django.urls import path
from users.views import SignUpCreateAPIView,  VerifyCodeAPIView, UpdateUserAPIView

app_name = "users"

urlpatterns = [
  path('register/' , SignUpCreateAPIView.as_view(), name='users_reg'),
  path('verify/', VerifyCodeAPIView.as_view(), name='verify'),
  path('update/', UpdateUserAPIView.as_view(), name='update_user'),
]