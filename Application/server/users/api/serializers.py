from django.contrib.auth.models import User

from rest_framework import serializers

class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'first_name', 'last_name')

class DetailUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'first_name', 'last_name')

class CreateUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = super(CreateUserSerializer, self).create(validated_data)
        user.set_password(validated_data.get('password'))
        user.save()

        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UpdateUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'email', 'first_name', 'last_name')
