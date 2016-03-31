from rest_framework import serializers
from django.contrib.auth.models import User
from establishments.models import Establishment

# from .models import UserProfile


class UserSerializer(serializers.HyperlinkedModelSerializer):
    establishments = serializers.HyperlinkedRelatedField(many=True, view_name='establishment-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'establishments')
        # fields = ('id', 'username', 'email', 'password', 'establishments')
    #     extra_kwargs = {'password': {'write_only': True}}
    #
    # def create(self, validated_data):
    #     user = User(
    #         email=validated_data['email'],
    #         username=validated_data['username']
    #     )
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user


# class UserProfileSerializer(serializers.ModelSerializer):
#
#     user = UserSerializer()
#
#     class Meta:
#         model = UserProfile
#         fields = ('id', 'spotify_username', 'user')
#
#     def create(self, validated_data):
#         user_profile = UserProfile(
#             spotify_username=validated_data['spotify_username'],
#         )
#         user_profile.save()
#         return user_profile
    # pk = serializers.IntegerField(read_only=True)
    # spotify_username = serializers.CharField(required=False, allow_blank=True, max_length=50)