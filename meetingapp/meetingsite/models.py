from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

class CustomUser(AbstractUser):
    
    GENDER_CHOICES = (
        ('мужчина', 'мужчина'),
        ('женщина', 'женщина')
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    age = models.PositiveSmallIntegerField(default=0)
    img = GenericRelation('meetingsite.Images')
    REQUIRED_FIELDS = ['gender', 'age', 'email']
    

class UserProfile(models.Model):

    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    bio = models.TextField(blank=True)
    img = GenericRelation('meetingsite.Images')


    def __str__(self):
        return f'{self.username}'


class Images(models.Model):

    image = models.ImageField(upload_to='user', default=None)

    object_id = models.IntegerField(null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    obj = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'{self.obj}'
