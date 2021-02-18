from django.contrib.contenttypes.models import ContentType
from rest_framework.response import Response

from profiles.models import FriendsProfile, DatesProfile
from profiles.serializers import (
    FriendsProfilesListSerializer,
    DatesProfilesListSerializer,
    FriendsProfileDetailSerializer,
    DatesProfileDetailSerializer,
    FriendsProfileInfoSerializer,
    DatesProfileInfoSerializer,
)


class ProfilesMixin:
    LIST_SERIALIZERS = {
        f'{FriendsProfile}': FriendsProfilesListSerializer,
        f'{DatesProfile}': DatesProfilesListSerializer,
    }
    DETAIL_SERIALIZERS = {
        f'{FriendsProfile}': FriendsProfileDetailSerializer,
        f'{DatesProfile}': DatesProfileDetailSerializer,
    }

    INFO_SERIALIZERS = {
        f'{FriendsProfile}': FriendsProfileInfoSerializer,
        f'{DatesProfile}': DatesProfileInfoSerializer,
    }

    def get_serializer_class(self, *args, **kwargs):
        ct_type = kwargs['ct_type']
        try:
            self.ct_model = ContentType.objects.get(pk=ct_type).model_class()
            serializer = kwargs['serializer_type'][str(self.ct_model)]
        except Exception:
            return Response(status=400, data="Incorrect Content Type")
        return serializer

    def get_queryset(self):
        return self.ct_model.objects.filter(is_active=True)
