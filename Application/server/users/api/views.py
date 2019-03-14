from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from . import serializers
from ..models import Profile

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
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UpdateUserSerializer
    
    def get_object(self):
        return self.request.user

class PasswordUpdateUserView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.PasswordUpdateUserSerializer

    def get_object(self):
        return self.request.user

class DestroyUserView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

class CurrentUserView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CurrentUserSerializer

    def get_object(self):
        return self.request.user

class ListProfileView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = serializers.ListProfileSerializer

class DetailProfileView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = serializers.DetailProfileSerializer

class CurrentProfileView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CurrentProfileSerializer

    def get_object(self):
        print(self.request.user)
        return self.request.user.profiles.first()

class UpdateProfileView(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UpdateProfileSerializer
    
    def get_object(self):
        return self.request.user.profiles.first()
