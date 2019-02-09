from django.contrib.auth.models import User

from rest_framework import serializers

class CreateUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return super(CreateUserSerializer, self).create(validated_data)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')