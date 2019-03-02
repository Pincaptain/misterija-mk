from django.contrib import admin

from .models import PostTopic, Post, PostImage, PostComment

admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(PostComment)
admin.site.register(PostTopic)