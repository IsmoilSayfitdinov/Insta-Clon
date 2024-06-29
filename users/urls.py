from django.urls import path
from users.views import SignUpCreateAPIView,  VerifyCodeAPIView, UpdateUserAPIView, UserAvatarUpdate, ResetPasswordView

app_name = "users"

urlpatterns = [
  path('register/' , SignUpCreateAPIView.as_view(), name='users_reg'),
  path('verify/', VerifyCodeAPIView.as_view(), name='verify'),
  path('update/', UpdateUserAPIView.as_view(), name='update_user'),
  path('update/avatar/', UserAvatarUpdate.as_view(), name='update_avatar'),
  path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
]