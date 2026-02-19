from django.contrib.auth import get_user_model,authenticate
from django.forms import fields
from rest_framework.fields import ReadOnlyField, SlugField
from .models import User
from django.contrib.auth.decorators import user_passes_test
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Follow

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ["id", "username", "email", "password", "bio", "profile_picture"]

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"],
            bio=validated_data.get("bio", ""),
            profile_picture=validated_data.get("profile_picture", None),
        )

        Token.objects.create(user=user)

        return user
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data["username"],
            password=data["password"]
        )

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        data["user"] = user
        return data

class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.ReadOnlyField(source = 'follower.username')
    following = serializers.SlugRelatedField(
        slug_field = 'username',
        queryset = User.objects.all()
    )
    class Meta:
        model = Follow
        fields = ['follower', 'following','created_at','id']
    def validate(self, data):
       if self.context['request'].user == data['following']:
           raise serializers.ValidationError("You cannot follow yourself")
       return data