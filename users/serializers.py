from rest_framework import serializers
from users.models import UserModel


class SignUpSerializer(serializers.ModelSerializer):
    def __init__(self):
        super(SignUpSerializer, self).__init__()
        self.fields['email_or_phone'] = serializers.CharField(max_length=256)
   
    
    class Meta:
        model = UserModel
        fields = ['uuid', 'auth_type', 'auth_status',] 
       

    def validate(self, attrs):
        return self.auth_validate(attrs)

    def create(self, validated_data):
        user = super(SignUpSerializer, self).create(validated_data)
        
        return user
    
    @staticmethod
    def auth_validate(data):
        user_input = data.get('email_or_phone', None)
        
        if user_input.endswith('@gmail.com'):
            data["email"] = user_input
            data["auth_type"] = UserModel.VIA_EMAIL
        elif user_input.startswith('+'):
            data["phone_number"] = user_input
            data["auth_type"] = UserModel.VIA_PHONE
        else:
            res = {
                'succses': False,
                'error': "Enter valid email or phone number"
            }
            
            raise serializers.ValidationError(res)