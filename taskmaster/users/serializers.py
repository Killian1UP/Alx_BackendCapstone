from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password'] # these are fields that will be exposed in the API
        extra_kwargs = {
            'password': {'write_only': True} # to ensure password is not readable in responses
        }

    # overidden the default create method to hash the passwords correctly
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user