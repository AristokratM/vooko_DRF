from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import FriendsProfile, Photo, Nationality, AcquaintanceRequest
from django.contrib.contenttypes.models import ContentType


class PhotoObjectRelatedSerializer(serializers.RelatedField):
    """
    A custom field to use for the `content_object` generic relationship.
    """

    def to_representation(self, value):

        if isinstance(value, FriendsProfile):
            serializers = FriendsProfilesListSerializer(value)
        else:
            return Exception("Unexpected type of tagged object")
        print(serializers.data)
        return serializers.data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name')


class PhotoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('id', 'photo')


class FriendsProfilesListSerializer(serializers.ModelSerializer):
    content_type = serializers.SerializerMethodField("get_content_type")
    age = serializers.SerializerMethodField("get_age_name")
    photos = PhotoListSerializer(many=True, read_only=True)
    user = UserSerializer()

    class Meta:
        model = FriendsProfile
        fields = ['id', 'content_type', 'user', 'photos', 'age', ]

    def get_age_name(self, obj):
        return obj.get_age(obj.birth_date)

    def get_content_type(self, obj):
        return ContentType.objects.get_for_model(FriendsProfile).pk


class PhotoDetailSerializer(serializers.ModelSerializer):
    # content_object = PhotoObjectRelatedSerializer(read_only=True)

    class Meta:
        model = Photo
        fields = '__all__'


class NationalityDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nationality
        fields = '__all__'


class NationalitiesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nationality
        fields = ('name',)


class AcquaintanceRequestsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcquaintanceRequest
        exclude = ('date',)


class AcquaintanceRequestDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcquaintanceRequest
        fields = '__all__'
