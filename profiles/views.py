from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import (
    FriendsProfile,
    Photo,
    Nationality,
    AcquaintanceRequest,
    Match,
    SexualOrientation,
    DatesProfile,
)
from .serializers import (
    FriendsProfilesListSerializer,
    PhotoListSerializer,
    PhotoDetailSerializer,
    NationalityDetailSerializer,
    NationalitiesListSerializer,
    AcquaintanceRequestsListSerializer,
    AcquaintanceRequestDetailSerializer,
    MatchDetailSerializer,
    MatchesListSerializer,
    SexualOrientationSerializer,
    DatesProfilesListSerializer,
    FriendsProfileDetailSerializer,
    DatesProfileDetailSerializer,
)
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType
from .mixins import ProfilesMixin


# Create your views here.

class FriendsProfilesListView(APIView):

    def get(self, request, *args, **kwargs):
        profiles = FriendsProfile.objects.all()
        serializer = FriendsProfilesListSerializer(profiles, many=True)
        return Response(serializer.data)


class PhotoListView(APIView):
    def get(self, request, *args, **kwargs):
        photos = Photo.objects.all()
        serializer = PhotoListSerializer(photos, many=True)
        return Response(serializer.data)

    def post(self, request, *arg, **kwargs):
        data = request.data
        serializer = PhotoDetailSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        return Response(status=406, data=serializer.errors)


class PhotoDetailView(APIView):
    def get(self, request, *args, **kwargs):
        photo = Photo.objects.get(pk=kwargs['pk'])
        serializer = PhotoDetailSerializer(photo)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        photo = Photo.objects.get(pk=kwargs['pk'])
        photo.delete()
        return Response(status=204)

    def put(self, request, *args, **kwargs):
        photo = Photo.objects.get(pk=kwargs['pk'])
        serializer = PhotoDetailSerializer(photo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=204)
        return Response(status=406, data=serializer.errors)


class NationalitiesListView(APIView):
    def get(self, request, *arg, **kwargs):
        nationalities = Nationality.objects.all()
        serializer = NationalitiesListSerializer(nationalities, many=True)
        return Response(data=serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = NationalityDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        return Response(status=406, data=serializer.errors)


class NatinalityDetailView(APIView):
    def get(self, request, *args, **kwargs):
        nationality = Nationality.objects.get(pk=kwargs['pk'])
        serializer = NationalityDetailSerializer(nationality)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        nationality = Nationality.objects.get(pk=kwargs['pk'])
        serializer = NationalityDetailSerializer(nationality, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=204)
        return Response(status=406, data=serializer.errors)

    def delete(self, request, *args, **kwargs):
        nationality = Nationality.objects.get(pk=kwargs['pk'])
        nationality.delete()
        return Response(status=204)


class AcquaintanceRequestsListView(APIView):
    def get(self, request, *args, **kwargs):
        acquaintance_requests = AcquaintanceRequest.objects.all()
        serializer = AcquaintanceRequestsListSerializer(acquaintance_requests, many=True)
        return Response(status=204, data=serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = AcquaintanceRequestDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        return Response(status=406, data=serializer.errors)


class AcquaintanceRequestDetailView(APIView):
    def get(self, request, *args, **kwargs):
        acquaintance_request = AcquaintanceRequest.objects.get(pk=kwargs['pk'])
        serializer = AcquaintanceRequestDetailSerializer(acquaintance_request)
        return Response(status=200, data=serializer.data)

    def put(self, request, *args, **kwargs):
        acquaintance_request = AcquaintanceRequest.objects.get(pk=kwargs['pk'])
        serializer = AcquaintanceRequestDetailSerializer(acquaintance_request, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=204)
        return Response(status=406, data=serializer.errors)

    def delete(self, request, *args, **kwargs):
        acquaintance_request = AcquaintanceRequest.objects.get(pk=kwargs['pk'])
        acquaintance_request.delete()
        return Response(status=204)


class MatchesListView(APIView):
    def get(self, request, *args, **kwargs):
        matches = Match.objects.all()
        serializer = MatchesListSerializer(matches, many=True)
        return Response(status=200, data=serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = MatchDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        return Response(status=406, data=serializer.data)


class MatchDetailView(APIView):
    def get(self, request, *args, **kwargs):
        match = Match.objects.get(pk=kwargs['pk'])
        serializer = MatchDetailSerializer(match)
        return Response(status=200, data=serializer.data)

    def put(self, request, *args, **kwargs):
        match = Match.objects.get(pk=kwargs['pk'])
        serializer = MatchDetailSerializer(match, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=204)
        return Response(status=406)

    def delete(self, request, *args, **kwargs):
        match = Match.objects.get(pk=kwargs['pk'])
        match.delete()
        return Response(status=204)


class SexualOrientationsListView(ListCreateAPIView):
    queryset = SexualOrientation.objects.all()
    serializer_class = SexualOrientationSerializer


class SexualOrientationDetailView(RetrieveUpdateDestroyAPIView):
    queryset = SexualOrientation.objects.all()
    serializer_class = SexualOrientationSerializer


class ProfilesListView(ProfilesMixin, APIView):

    def get(self, request, *args, **kwargs):
        kwargs['serializer_type'] = self.LIST_SERIALIZERS
        serializer_class = self.get_serializer_class(*args, **kwargs)
        serializer = serializer_class(self.get_queryset(), many=True)
        return Response(status=200, data=serializer.data)

    def post(self, request, *args, **kwargs):
        kwargs['serializer_type'] = self.DETAIL_SERIALIZERS
        serializer_class = self.get_serializer_class(*args, **kwargs)
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201, data=serializer.data)
        return Response(status=406, data=serializer.errors)


class ProfileDetailView(ProfilesMixin, APIView):
    def get(self, request, *args, **kwargs):
        kwargs['serializer_type'] = self.DETAIL_SERIALIZERS
        serializer_class = self.get_serializer_class(*args, **kwargs)
        queryset = self.ct_model.objects.get(pk=kwargs['pk'])
        serializer = serializer_class(queryset)
        return Response(status=200, data=serializer.data)

