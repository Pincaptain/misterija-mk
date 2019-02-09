from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from . import serializers

class ListUserView(generics.ListAPIView):

    queryset = User.objects.all()
    serializer_class = serializers.ListUserSerializer

class DetailUserView(generics.RetrieveAPIView):

    queryset = User.objects.all()
    serializer_class = serializers.DetailUserSerializer

class CreateUserView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = serializers.CreateUserSerializer

class UpdateUserView(generics.UpdateAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UpdateUserSerializer
    
    def get_object(self):
        return self.request.user

class CurrentUserView(generics.RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CurrentUserSerializer

    def get_object(self):
        return self.request.user