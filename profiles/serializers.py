from rest_framework import serializers
from .models import Profile


class ProfilesListSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField("get_age_name")

    class Meta:
        model = Profile
        fields = ['id', 'user', 'photos', 'age']

    def get_age_name(self, obj):
        return obj.get_age()

