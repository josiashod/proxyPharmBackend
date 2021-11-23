import random
import string

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        Group, Permission, PermissionsMixin)
from django.db import models

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username, person, password=None):

        u = self.model(
            username= username,
            person= person,
        )

        u.set_password(password)
        u.save(using=self._db)

        return u

    def create_superuser(self, username, person= None, password= None):

        u = self.create_user(
            username= username,
            person= person
        )

        u.set_password(password)
        u.is_superuser = True
        u.save(using=self._db)

        return u

class Person(models.Model):
    first_name = models.CharField(max_length= 255)
    last_name = models.CharField(max_length= 255, null=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    phone = models.CharField(max_length= 255, null=True, blank=True, unique=True)
    image = models.FileField(null= True, blank= True, default= None)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(default= None, null= True)

    def get_full_name(self):
        return f"{ self.first_name } { self.last_name }"

class User(AbstractBaseUser, PermissionsMixin, models.Model):
    username = models.CharField(max_length=254, unique=True)
    person = models.OneToOneField(to= Person, null= True, blank= True, on_delete= models.DO_NOTHING)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(default= None, null= True)
    last_login = models.DateTimeField(default= None, null= True)

    def has_module_perms(self, admin):
        return True

    def __unicode__(self):
        return self.username

    objects = UserManager()

    USERNAME_FIELD = 'username'

    # REQUIRED_FIELDS = ['first_name', 'last_name']

    @property
    def is_staff(self):
        return self.is_superuser

    # class Meta:
    #     permissions = [
    #         ("can_edit_blog", "Can edit blog article, delete and view"),
    #         ("can_affiliated", "Can affiliate person to a sponsor"),
    #         ("can_administrate", "Can administrate the website"),
    #     ]

class Token(models.Model):
    user = models.OneToOneField(to= User, on_delete= models.DO_NOTHING)
    digest = models.CharField(max_length= 255, null= True)
    expire_at = models.DateTimeField(null= True)
    confirmed_at = models.DateTimeField(null= True)

    def generate_digest(self, number= True, length= None):
        if not number and length is None:
            raise Exception('Function parse error')
            
        if number:
            return random.randint(100000,999999+1)
        else:
            return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))

class Connection(models.Model):
    ip = models.GenericIPAddressField(null= True)
    device = models.CharField(max_length= 255, null= True)
    location = models.CharField(max_length= 255, null= True)
    login_at = models.DateTimeField(null= True)
    user = models.ForeignKey(to= User, null= True, blank= True, on_delete= models.DO_NOTHING)
