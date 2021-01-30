from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import FriendsProfile, Photo
from django.contrib.contenttypes.models import ContentType


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name')


class PhotoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('id', 'photo')


class PhotoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'


class FriendsProfilesListSerializer(serializers.ModelSerializer):
    content_type = serializers.SerializerMethodField("get_content_type")
    age = serializers.SerializerMethodField("get_age_name")
    photos = serializers.SerializerMethodField("get_friends_profile_photos")
    user = UserSerializer()

    class Meta:
        model = FriendsProfile
        fields = ['id', 'content_type', 'user', 'photos', 'age', ]

    def get_age_name(self, obj):
        return obj.get_age(obj.birth_date)

    def get_friends_profile_photos(self, obj):
        return PhotoListSerializer(self.context['photos'].filter(object_id=obj.id), many=True).data

    def get_content_type(self, obj):
        return ContentType.objects.get_for_model(FriendsProfile).pk
