from django.contrib.auth.models import User

from rest_framework import serializers

from ..models import Profile

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

    new_password = serializers.CharField(write_only=True)
    current_password = serializers.CharField(write_only=True)

    def validate(self, data):
        errors = {}
        new_password = data.get('new_password')
        current_password = data.get('current_password')

        if new_password is None:
            errors['new_password'] = 'This field is required'

        if current_password is None:
            errors['current_password'] = 'This field is required'

        user = self.instance

        if not user.check_password(current_password) and 'current_password' not in errors.keys():
            errors['current_password'] = 'Current password is invalid'

        if len(errors.keys()) != 0:
            raise serializers.ValidationError(errors)

        return data

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        user.set_password(validated_data.get('new_password'))
        user.save()

        return user

    class Meta:
        model = User
        fields = ('pk', 'username', 'new_password', 'current_password')
        read_only_fields = ('pk', 'username')

class ListProfileSerializer(serializers.ModelSerializer):
    user = DetailUserSerializer(many=False, read_only=True)

    class Meta:
        model = Profile
        fields = ('bio', 'location', 'avatar', 'user')

class DetailProfileSerializer(serializers.ModelSerializer):
    user = DetailUserSerializer(many=False, read_only=True)

    class Meta:
        model = Profile
        fields = ('pk', 'bio', 'location', 'avatar', 'user')

class CurrentProfileSerializer(serializers.ModelSerializer):
    user = CurrentUserSerializer(many=False, read_only=True)

    class Meta:
        model = Profile
        fields = ('pk', 'bio', 'location', 'avatar', 'user')
