from django.urls import path
from users.views import (
  SignUpCreateAPIView,  VerifyCodeAPIView,
  UpdateUserAPIView, UserAvatarUpdate,
  ResetPasswordView, LoginUserApiView,
  LogoutVIEW, GetReturnRefereshTokenAPIView, MyAccountView
)


urlpatterns = [
  path("refresh/", GetReturnRefereshTokenAPIView.as_view(), name="refresh"),
  path('register/' , SignUpCreateAPIView.as_view(), name='users_reg'),
  path('login/', LoginUserApiView.as_view(), name='login'),
  path('logout/', LogoutVIEW.as_view(), name='logout'),
  path('verify/', VerifyCodeAPIView.as_view(), name='verify'),
  path('update/', UpdateUserAPIView.as_view(), name='update_user'),
  path('update/avatar/', UserAvatarUpdate.as_view(), name='update_avatar'),
  path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
  path('myaccount/', MyAccountView.as_view(), name='my_account'),
]