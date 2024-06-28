from django.shortcuts import render
from users.serializers import SignUpSerializer, ResetPasswordSerializer, UpdateUserSerializer, UpdateAvatarUser
from users.models import UserModel, ConfimationModel, CODE_VERIFIED, DONE
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from rest_framework import status

class SignUpCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer
    model = UserModel
    
class VerifyCodeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        code = request.data.get('code')

        verification_code = ConfimationModel.objects.filter(
            user=user.id, code=code, is_confirmed=False, expiration_time__gte=timezone.now())
        if verification_code.exists():
            user.auth_status = CODE_VERIFIED
            user.save()

            verification_code.update(is_confirmed=True)

            response = {
                'success': True,
                'message': "Your code is successfully verified.",
                'auth_status': CODE_VERIFIED,
                'access_token': user.token()['access_token']
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                'success': False,
                'message': "Your code is invalid or already expired"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    

class UpdateUserAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UpdateUserSerializer
    http_method_names = ['patch', 'put']

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        super(UpdateUserAPIView, self).update(request, *args, **kwargs)
        data = {
            'success': True,
            "message": "User updated successfully",
            'auth_status': self.request.user.auth_status,
        }
        return Response(data, status=200)

    def partial_update(self, request, *args, **kwargs):
        super(UpdateUserAPIView, self).partial_update(request, *args, **kwargs)
        data = {
            'success': True,
            "message": "User updated successfully",
            'auth_status': self.request.user.auth_status,
        }
        return Response(data, status=200)
    
class UserAvatarUpdate(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, requset, *args, **kwargs):
        serializers = UpdateAvatarUser(data=requset.data)
        if serializers.is_valid():
            user = requset.user
            serializers.update(user, serializers.validated_data)
            res = {
                'success': True,
                'message': 'User avatar updated successfully',
                'avatar': user.avatar.url
            }
            return Response(res)        
        return Response(serializers.errors , status=status.HTTP_400_BAD_REQUEST)
    
class ResetPasswordView(UpdateAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [IsAuthenticated, ]
    http_method_names = ['patch', 'put']

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        response = super(ResetPasswordView, self).update(request, *args, **kwargs)
        try:
            user = UserModel.objects.get(id=response.data.get('id'))
        except:
            raise Response({'success': False, 'message': 'User not found'}, status='User not found')
        return Response(
            {
                'success': True,
                'message': "Parolingiz muvaffaqiyatli o'zgartirildi",
                'access': user.token()['access'],
                'refresh': user.token()['refresh_token'],
            }
        )