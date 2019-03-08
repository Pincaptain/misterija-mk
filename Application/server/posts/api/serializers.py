from django.apps import apps

from rest_framework import serializers

from ..models import PostTopic, PostImage, Post, PostComment
from users.api.serializers import DetailProfileSerializer

class ListPostTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTopic
        fields = ('pk', 'name')

class DetailPostTopicSerializier(serializers.ModelSerializer):
    class Meta:
        model = PostTopic
        fields = ('pk', 'name')

class DetailPostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ('pk', 'image')

class DetailPostCommentSerializer(serializers.ModelSerializer):
    author_profile = DetailProfileSerializer(many=False, read_only=True)

    class Meta:
        model = PostComment
        fields = ('pk', 'comment', 'added', 'author_profile', 'selected', 'votes_count')

class CreatePostCommentSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        validated_data['author'] = user
        comment = super().create(validated_data)

        return comment

    class Meta:
        model = PostComment
        fields = ('comment', 'post')

class UpdatePostCommentSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        request = self.context['request']
        user = request.user

        if self.instance.author != user:
            raise serializers.ValidationError('That is not your comment to remove')

        return super().validate(attrs)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    class Meta:
        model = PostComment
        fields = ('comment',)

class ListPostSerializer(serializers.ModelSerializer):
    topics = DetailPostTopicSerializier(many=True, read_only=True)
    author_profile = DetailProfileSerializer(many=False, read_only=True)

    class Meta:
        model = Post
        fields = ('pk', 'title', 'description', 'difficulty', 'added', 'thumbnail', 'topics', 'author_profile', 'comments_count')

class DetailPostSerializer(serializers.ModelSerializer):
    topics = DetailPostTopicSerializier(many=True, read_only=True)
    author_profile = DetailProfileSerializer(many=False, read_only=True)
    images = DetailPostImageSerializer(many=True, read_only=True)
    comments = DetailPostCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('pk', 'title', 'description', 'difficulty', 'added', 'thumbnail', 'topics', 'author_profile', 'images', 'comments')