from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        # normalize_email로 email 정규화 (
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password,**extra_fields):
        user = self.create_user(email, password, **extra_fields)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email,password,**extra_fields)

class User(AbstractBaseUser,PermissionsMixin):
    username = models.CharField('이름',max_length=100,unique=True)
    email = models.EmailField(verbose_name='이메일',max_length=100,unique=True)
    # password = models.CharField('비밀번호',max_length=100)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @property
    def is_superuser(self):
        return self.is_admin

