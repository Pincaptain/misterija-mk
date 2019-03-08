from django.shortcuts import get_object_or_404

from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response

from . import serializers
from ..models import PostTopic, PostComment, Post

class ListPostTopicView(ListAPIView):
    queryset = PostTopic.objects.all()
    serializer_class = serializers.ListPostTopicSerializer

class DetailPostTopicView(RetrieveAPIView):
    queryset = PostTopic.objects.all()
    serializer_class = serializers.DetailPostTopicSerializier

class CreatePostCommentView(CreateAPIView):
    queryset = PostComment.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CreatePostCommentSerializer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        return context
    
class UpdatePostCommentView(UpdateAPIView):
    queryset = PostComment.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UpdatePostCommentSerializer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        return context

class DestroyPostCommentView(DestroyAPIView):
    queryset = PostComment.objects.all()
    permission_classes = (IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        if instance.author != user:
            raise ValidationError('That is not your comment to destroy')

        return super().destroy(request, *args, **kwargs)

class VotePostCommentView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        user = request.user
        comment = get_object_or_404(PostComment, pk=pk)

        if user in comment.votes.all():
            comment.votes.remove(user)
        else:
            comment.votes.add(user)

        comment.save()

        serializer = serializers.DetailPostCommentSerializer(comment, many=False)

        return Response(serializer.data)

class ListPostView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.ListPostSerializer

class DetailPostView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.DetailPostSerializer
