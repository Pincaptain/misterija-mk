from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.db import models
from django.core.files.storage import default_storage
from django.conf import settings

from rest_framework.authtoken.models import Token

import os
import uuid
import random
from shutil import copyfile

def get_default_avatar_path():
    media_path = settings.MEDIA_ROOT
    defaults_path = os.path.join(media_path, 'users', 'avatars', 'defaults')
    directory = os.listdir(defaults_path)
    count = len(directory)
    index = random.randint(0, count-1)
    extension = 'png'
    filename = '{0}.{1}'.format(str(index), extension)
    src = os.path.join(defaults_path, filename)
    filename = '{0}.{1}'.format(uuid.uuid4(), extension)
    dst = os.path.join(media_path, 'users', 'avatars', filename)

    copyfile(src, dst)

    return os.path.join('users', 'avatars', filename)

def get_avatar_path(instance, filename):
    extension = filename.split('.')[-1]
    filename = '{0}.{1}'.format(uuid.uuid4(), extension)

    return os.path.join('users/avatars', filename)

class Profile(models.Model):
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=60, blank=True)
    avatar = models.ImageField(upload_to=get_avatar_path, default=get_default_avatar_path, blank=True, max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profiles')

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

@receiver(pre_save, sender=Profile)
def delete_current_avatar(sender, **kwargs):
    instance = kwargs['instance']

    if instance.pk:
        profile = Profile.objects.get(pk=instance.pk)

        if instance.avatar != profile.avatar:
            profile.avatar.delete(save=False)

@receiver(post_delete, sender=Profile)
def delete_avatar(sender, **kwargs):
    instance = kwargs['instance']
    instance.avatar.delete(save=False)
