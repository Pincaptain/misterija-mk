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

class PasswordUpdateUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    old_password = serializers.CharField(write_only=True)

    def validate(self, data):
        super().validate(data)

        password = data.get('password')
        old_password = data.get('old_password')

        if password is None or password is '':
            raise serializers.ValidationError('New password is required')

        if old_password is None or old_password == '':
            raise serializers.ValidationError('Current password is required')

        user = self.instance

        if not user.check_password(old_password):
            raise serializers.ValidationError('Your current password is invalid')

        return data

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        user.set_password(validated_data.get('password'))
        user.save()

        return user

    def validate_old_password(self, value):
        user = self.instance

        if value is None or value == '':
            raise serializers.ValidationError('Current password is required')

        if not user.check_password(value):
            raise serializers.ValidationError('Your current password is invalid')

        return value

    class Meta:
        model = User
        fields = ('password', 'old_password')
