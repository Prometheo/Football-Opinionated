from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer

from football_opinionated.users.models import User

#used to serialize the folowers count
class HelperSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "name",
            "country",
        ]


#a user serializer obviously
class UserSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()
    followed_by = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "name",
            "url",
            "fav_team",
            "country",
            'followers',
            'followed_by'
            ]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }

# get the list of people the user is following
    def get_followers(self, obj):
        folowers = HelperSerializer(obj.friends.all(), many=True).data
        return folowers

# get the list of people following the user
    def get_followed_by(self, obj):
        following = HelperSerializer(obj.followers.all(), many=True).data
        return following


class CustomRegisterSerializer(RegisterSerializer):
    full_name = serializers.CharField(required=True)

    def get_cleaned_data(self):
        return {
            'name': self.validated_data.get('full_name'),
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', '')
        }

