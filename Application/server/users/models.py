from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models

from rest_framework.authtoken.models import Token

import os
import uuid

def get_avatar_path(instance, filename):
    extension = filename.split('.')[-1]
    filename = '{0}.{1}'.format(uuid.uuid4(), extension)

    return os.path.join('users/avatars', filename)

class Profile(models.Model):

    bio = models.TextField(blank=True)
    location = models.CharField(max_length=60, blank=True)
    avatar = models.ImageField(upload_to=get_avatar_path, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles' 
    

@receiver(post_save, sender=User)
def create_token(sender, **kwargs):
    if kwargs['created']:
        Token.objects.create(user=kwargs['instance'])

@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])
