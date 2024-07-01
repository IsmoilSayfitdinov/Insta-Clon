from rest_framework import serializers
from users.models import UserModel
from users.models import VIA_EMAIL, VIA_PHONE, CODE_VERIFIED, DONE, PHOTO
from shared.utils import send_code_to_email, send_code_to_phone
from django.contrib.auth.password_validation import validate_password
from django.core.validators import FileExtensionValidator
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
import re
from django.contrib.auth import get_user_model

COUNTRY_CODES = [
    "+1", "+7", "+86", "+81", "+82", "+91", "+92", "+998", "+49", "+33", "+44", "+39", "+34", "+90", "+20", "+966",
]


def validator_email_and_phone(value):
    phone_regex = r'^\+?1?\d{9,15}$'
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    if value.startswith('+') and  any(value.startswith(code) for code in COUNTRY_CODES):
        if not re.match(phone_regex, value):
            raise serializers.ValidationError('Phone number error')
    
   
    else:
        if not re.match(email_regex, value):
            raise serializers.ValidationError('Invalid email address')

class SignUpSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(SignUpSerializer, self).__init__(*args, **kwargs)
        self.fields['email_phone_number'] = serializers.CharField(validators=[validator_email_and_phone],max_length=128, required=False)

    uuid = serializers.IntegerField(read_only=True)
    auth_type = serializers.CharField(read_only=True, required=False)
    auth_status = serializers.CharField(read_only=True, required=False)

    class Meta:
        model = UserModel
        fields = ['uuid', 'auth_type', 'auth_status']

    def validate(self, data):
        data = self.auth_validate(data=data)
        return data

    def create(self, validated_data):
        user = super(SignUpSerializer, self).create(validated_data)
        code = user.create_verify_code(user.auth_type)

        if user.auth_type == VIA_EMAIL:
            send_code_to_email(user.email, code)
        else:
            send_code_to_phone(phone_number=user.phone_number, code=code)
        user.save()
        return user

    @staticmethod
    def auth_validate(data):
        user_input = str(data['email_phone_number']).lower()
        if user_input.endswith('@gmail.com'):
            data = {
                'email': user_input,
                'auth_type': VIA_EMAIL
            }
        elif user_input.startswith("+") or user_input.startswith("+998"):
            data = {
                'phone_number': user_input,
                'auth_type': VIA_PHONE
            }
        else:
            data = {
                'success': False,
                'message': "Please enter a valid phone number or email"
            }
            raise serializers.ValidationError(data)
        return data

    def to_representation(self, instance):
        data = super(SignUpSerializer, self).to_representation(instance)
        data['access_token'] = instance.token()['access_token']
        return data



class UpdateUserSerializer(serializers.Serializer):
    first_name = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        password = data.get('password', None)
        confirm_password = data.get('confirm_password', None)
        if password !=confirm_password:
            raise serializers.ValidationError(
                {
                    "message": "Parolingiz va tasdiqlash parolingiz bir-biriga teng emas"
                }
            )
        if password:
            validate_password(password)
            validate_password(confirm_password)

        return data

    def validate_username(self, username):
        if len(username) < 5 or len(username) > 30:
            raise serializers.ValidationError(
                {
                    "message": "Username must be between 5 and 30 characters long"
                }
            )
        if username.isdigit():
            raise serializers.ValidationError(
                {
                    "message": "This username is entirely numeric"
                }
            )
        return username

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.password = validated_data.get('password', instance.password)
        instance.username = validated_data.get('username', instance.username)
        
        if validated_data.get('password'):
            instance.set_password(validated_data.get('password'))
        if instance.auth_status == CODE_VERIFIED:
            instance.auth_status = DONE
            
        instance.save()
        return instance




class UpdateAvatarUser(serializers.Serializer):
    avatar = serializers.ImageField(validators=[FileExtensionValidator(allowed_extensions=[
        'jpg', 'jpeg', 'png', 'pdf'
    ])])
    
    def update(self, instance, validated_data):
        avatar = validated_data.get("avatar")
        
        if avatar:
            instance.avatar = avatar
            instance.auth_status = PHOTO
            instance.save()
            
        return instance
    
    
class ResetPasswordSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    password = serializers.CharField(min_length=8, required=True, write_only=True)
    confirm_password = serializers.CharField(min_length=8, required=True, write_only=True)

    class Meta:
        model = UserModel
        
        fields = (
            'id',
            'password',
            'confirm_password'
        )

    def validate(self, data):
        
        password = data.get('password', None)
        confirm_password = data.get('password', None)
        
        if password != confirm_password:
            raise serializers.ValidationError(
                {
                    'success': False,
                    'message': "Parollaringiz qiymati bir-biriga teng emas"
                }
            )
            
        if password:
            validate_password(password)
            
        return data

    def update(self, instance, validated_data):
        
        password = validated_data.pop('password')
        instance.set_password(password)
        return super(ResetPasswordSerializer, self).update(instance, validated_data)
    
    

class Loginsrerialziers(TokenObtainPairSerializer):
    
    def __init__(self, *args, **kwargs):
        super(Loginsrerialziers, self).__init__(*args, **kwargs)
        self.fields['userinput'] = serializers.CharField(max_length=128, required=False)
        self.fields["username"] = serializers.CharField(max_length=128, required=False) 
        
    def validate(self, attrs):
        userinput = attrs.get("userinput")
            
        if userinput.endswith("@gmail.com"):
            user = UserModel.objects.filter(email=userinput).first()
                
        elif userinput.startswith("+998") or userinput.startswith("+"):
            user = UserModel.objects.filter(phone_number=userinput).first()
            
        else:
            user = UserModel.objects.filter(username=userinput).first()
        if user is None:
            raise serializers.ValidationError({
                "success": False,
                "message": "User not found"
                })
        
        auth_user = authenticate(username=user.username, password=attrs.get("password"))
        if auth_user is None:
            raise serializers.ValidationError({
                "success": False,
                "message": "Username or password not found"
                })
        
        if user.auth_status == PHOTO or user.auth_status == DONE:
            res =  {
            'success': True,
            'access_token': auth_user.token()['access_token'],
            'refresh_token': auth_user.token()['refresh_token'],
            }
        
        else:
            res = {
                "success": False,
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Your status not PHOTO or DONE"
            }
            
        
            
        return res
        
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()