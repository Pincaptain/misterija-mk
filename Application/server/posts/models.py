import os
import uuid
import random
from shutil import copyfile

from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings

class PostTopic(models.Model):
    name = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Post Topic'
        verbose_name_plural = 'Post Topics'

def get_post_thumbnail(instance, filename):
    extension = filename.split('.')[-1]
    filename = '{0}.{1}'.format(uuid.uuid4(), extension)

    return os.path.join('posts/thumbnails', filename)

class Post(models.Model):
    title = models.CharField(max_length=60, unique=True)
    description = models.TextField()
    difficulty = models.FloatField(default=0.5)
    added = models.DateTimeField(auto_now_add=True)
    topics = models.ManyToManyField(PostTopic, related_name='posts', related_query_name='post')
    thumbnail = models.ImageField(upload_to=get_post_thumbnail, null=True, blank=True, max_length=255)
    author = models.ForeignKey(User, related_name='posts', related_query_name='post', on_delete=models.CASCADE)

    @property
    def author_profile(self):
        return self.author.profiles.first()

    @property
    def comments_count(self):
        return len(self.comments.all())

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-added']

@receiver(post_delete, sender=Post)
def delete_thumbnail(sender, **kwargs):
    instance = kwargs['instance']
    instance.thumbnail.delete(save=False)

@receiver(pre_save, sender=Post)
def delete_current_thumbnail(sender, **kwargs):
    instance = kwargs['instance']

    if instance.pk:
        post = Post.objects.get(pk=instance.pk)

        if instance.thumbnail != post.thumbnail:
            post.thumbnail.delete(save=False)

def get_post_image_path(instance, filename):
    extension = filename.split('.')[-1]
    filename = '{0}.{1}'.format(uuid.uuid4(), extension)

    return os.path.join('posts/images', filename)

class PostImage(models.Model):
    image = models.ImageField(upload_to=get_post_image_path, max_length=255)
    post = models.ForeignKey(Post, related_name='images', related_query_name='image', on_delete=models.CASCADE)

    def __str__(self):
        return '{0} - {1}'.format(self.post.title, self.pk)

    class Meta:
        verbose_name = 'Post Image'
        verbose_name_plural = 'Post Images'

@receiver(post_delete, sender=PostImage)
def delete_image(sender, **kwargs):
    instance = kwargs['instance']
    instance.image.delete(save=False)

@receiver(pre_save, sender=PostImage)
def delete_current_image(sender, **kwargs):
    instance = kwargs['instance']

    if instance.pk:
        post_image = PostImage.objects.get(pk=instance.pk)

        if instance.image != post_image.image:
            post_image.image.delete(save=False)

class PostComment(models.Model):
    comment = models.TextField()
    added = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, related_name='comments', related_query_name='comment', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', related_query_name='comment', on_delete=models.CASCADE)
    selected = models.BooleanField(default=False)
    votes = models.ManyToManyField(User, related_name='voted_comments', related_query_name='voted_comment', blank=True)

    @property
    def author_profile(self):
        return self.author.profiles.first()
    
    @property
    def votes_count(self):
        return len(self.votes.all())

    def __str__(self):
        return '{0} - {1}'.format(self.post.title, self.pk)

    class Meta:
        verbose_name = 'Post Comment'
        verbose_name_plural = 'Post Comments'
        ordering = ['-added']
