from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import (
    FriendsProfile,
    Photo,
    Nationality,
    AcquaintanceRequest,
    DatesProfile,
    Match,
    SexualOrientation,
)
from django.contrib.contenttypes.models import ContentType


class PhotoObjectRelatedSerializer(serializers.RelatedField):
    """
    A custom field to use for the `content_object` generic relationship.
    """

    def to_representation(self, value):

        if isinstance(value, FriendsProfile):
            serializers = FriendsProfilesListSerializer(value)
        elif isinstance(value, DatesProfile):
            serializers = DatesProfilesListSerializer(value)
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
    age = serializers.SerializerMethodField("get_age_name")
    photos = PhotoListSerializer(many=True, read_only=True)
    user = UserSerializer()

    class Meta:
        model = FriendsProfile
        fields = ['id', 'user', 'photos', 'age', ]

    def get_age_name(self, obj):
        return obj.get_age(obj.birth_date)


class PhotoDetailSerializer(serializers.ModelSerializer):
    content_object = PhotoObjectRelatedSerializer(read_only=True, )

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
        exclude = ('request_date',)


class AcquaintanceRequestDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcquaintanceRequest
        fields = '__all__'


class MatchesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        exclude = ('match_date', )


class MatchDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'

    def create(self, validated_data):
        dict = {
            'content_type': validated_data.get('content_type'),
            'sender_object_id': validated_data.get('initiator_object_id'),
            'receiver_object_id': validated_data.get('confirmer_object_id'),
        }
        if AcquaintanceRequest.objects.filter(**dict).count() == 0:
            raise serializers.ValidationError("There is no corresponding acquaintance request")
        return Match.objects.create(**validated_data)


class SexualOrientationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SexualOrientation
        fields = '__all__'


class DatesProfilesListSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField("get_age_name")
    photos = PhotoListSerializer(many=True, read_only=True)
    user = UserSerializer()

    class Meta:
        model = DatesProfile
        fields = ['id', 'user', 'photos', 'age', ]

    def get_age_name(self, obj):
        return obj.get_age(obj.birth_date)


class DatesProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatesProfile
        fields = '__all__'


class FriendsProfileDetailSerializer(serializers.ModelSerializer):
    photos = PhotoListSerializer(many=True, read_only=True)
    initiated_matches = MatchesListSerializer(many=True, read_only=True)
    confirmed_matches = MatchesListSerializer(many=True, read_only=True)
    sent_requests = AcquaintanceRequestsListSerializer(many=True, read_only=True)
    received_requests = AcquaintanceRequestsListSerializer(many=True, read_only=True)

    class Meta:
        model = FriendsProfile
        fields = '__all__'
