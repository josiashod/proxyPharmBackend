from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import Group, Permission
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE


# Create your models here.

class AbstractClass():
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default= None)

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

class Person(SafeDeleteModel, AbstractClass):
    _safedelete_policy = SOFT_DELETE_CASCADE

    first_name = models.CharField(max_length= 255)
    last_name = models.CharField(max_length= 255, null=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    phone = models.CharField(max_length= 255, null=True, blank=True, unique=True)
    is_user = models.BooleanField(default=True)
    is_pharmacist = models.BooleanField(default=False)

    def get_full_name(self):
        return f"{ self.first_name } { self.last_name }"

class User(AbstractBaseUser, PermissionsMixin, AbstractClass):
    username = models.TextField(max_length=254, unique=True)
    person = models.OneToOneField(to= Person, null= True, blank= True, on_delete= models.DO_NOTHING)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

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

class Connection(SafeDeleteModel, AbstractClass):
    ip = models.GenericIPAddressField(null= True)
    device = models.CharField(max_length= 255, null= True)
    location = models.CharField(max_length= 255, null= True)
    login_at = models.DateTimeField(null= True)
    user = models.ForeignKey(to= User, null= True, blank= True, on_delete= models.DO_NOTHING)