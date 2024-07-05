from django.db import models
from django.contrib.auth.models import AbstractUser
from shared.models import BaseModel
import uuid
from django.utils import timezone
import random
from rest_framework_simplejwt.tokens import RefreshToken

VIA_EMAIL, VIA_PHONE = "VIA_EMAIL", "VIA_PHONE"
ORDINARY_USER, MANAGER, ADMIN = "ORDINARY_USER", "MANAGER", "ADMIN"
NEW, CODE_VERIFIED, DONE, PHOTO = "NEW", "CODE_VERIFIED", "DONE", "PHOTO"


class UserModel(AbstractUser, BaseModel):
    AUTH_TYPES = (
        (VIA_EMAIL, VIA_EMAIL),
        (VIA_PHONE, VIA_PHONE),
    )
    
    AUTH_STATUS = (
        (NEW, NEW),
        (CODE_VERIFIED, CODE_VERIFIED),
        (DONE, DONE),
        (PHOTO, PHOTO),
    )
    
    USER_ROLES = (
        (ORDINARY_USER, ORDINARY_USER),
        (MANAGER, MANAGER),
        (ADMIN, ADMIN),
    )
    
    auth_type = models.CharField(max_length=128, choices=AUTH_TYPES, default=VIA_EMAIL)
    auth_status = models.CharField(max_length=128, choices=AUTH_STATUS, default=NEW)
    user_role = models.CharField(max_length=128, choices=USER_ROLES, default=ORDINARY_USER)

    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=13, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatar',null=True, blank=True)
    
    def __str__(self):
        return self.username
    
    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"
        
    def check_username(self):
        if not self.username:
            temp_username = F"instagram-{uuid.uuid4()}"
            while UserModel.objects.filter(username=temp_username).exists():
                self.check_username()
            self.username = temp_username
    
    def check_pass(self):
        if not self.password:
            self.password = f"password-{uuid.uuid4()}"
    
    def check_email(self):
        self.email = str(self.email).lower()
    
    def hashing_password(self):
        if not self.password.startswith('pbkdf2_sha256'):
            self.set_password(self.password)
    
    def clean(self):
        self.check_username()
        self.check_pass()
        self.check_email()
        self.hashing_password()
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.clean()
        super(UserModel, self).save(*args, **kwargs)
        
    def create_verify_code(self, verify_type):
        code = "".join([str(random.randint(1, 100) % 10) for _ in range(4)])
        ConfimationModel.objects.create(
            code=code,
            user=self,
            verify_type=verify_type
        )
        return code
    
    
    def token(self):
        refresh_token = RefreshToken.for_user(self)
        
        response = {
            'access_token': str(refresh_token.access_token),
            'refresh_token': str(refresh_token)
        }
        
        return response
        

EMAIL_VERFIY_TIME = 4
PHONE_VERFIY_TIME = 2
    
    
class ConfimationModel(BaseModel):
    verify_type = (
        (VIA_EMAIL, VIA_EMAIL),
        (VIA_PHONE, VIA_PHONE),
    )
    code = models.CharField(max_length=4)
    verify_type = models.CharField(max_length=128, choices=verify_type, default=VIA_EMAIL)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='verification_code')
    expiration_time = models.DateTimeField()
    is_confirmed = models.BooleanField(default=False)
    
    
    def save(self, *args, **kwargs):
        if not self.pk:
            if self.verify_type == VIA_EMAIL:
                self.expiration_time = timezone.now() + timezone.timedelta(minutes=EMAIL_VERFIY_TIME)
            else:
                self.expiration_time = timezone.now() + timezone.timedelta(minutes=PHONE_VERFIY_TIME)
                
        super(ConfimationModel, self).save(*args, **kwargs)
        

