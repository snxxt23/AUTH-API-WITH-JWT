from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager


#custom_manager
class UserManager(BaseUserManager):
    def create_user(self,username,email,password=None,**extra_fields):
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,username,email,password=None):
        user = self.create_user(username,email,password=password)
        user.is_admin=True
        user.save(using=self._db)
        return user


#custom_user 
class User(AbstractBaseUser):
    username = models.CharField(max_length=200)
    email = models.EmailField(max_length=200,unique=True,verbose_name='Email',)
    first_name = models.CharField(max_length=200,null=True,blank=True)
    last_name = models.CharField(max_length=200,null=True,blank=True)
    profile_picture = models.ImageField(upload_to='profile_photo/',null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    def __str__(self):
        return self.username

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def has_perm(self,perm,obj=None):
        "Does this user have a specific permission?"
        return self.is_admin

    def has_module_perms(self,app_label):
        "Does this user have permission to view the app'app_label'?"
        return True


    @property
    def is_staff(self):
        "is this user a member of staff"
        return self.is_admin
