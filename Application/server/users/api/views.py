from django.contrib.auth.models import User

from rest_framework import generics

from . import serializers

class CreateUserView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = serializers.CreateUserSerializer