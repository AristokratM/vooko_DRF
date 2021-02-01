from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from .models import FriendsProfile, Photo, Nationality, AcquaintanceRequest
from .serializers import (
    FriendsProfilesListSerializer,
    PhotoListSerializer,
    PhotoDetailSerializer,
    NationalityDetailSerializer,
    NationalitiesListSerializer,
    AcquaintanceRequestsListSerializer,
    AcquaintanceRequestDetailSerializer
)
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType


# Create your views here.

class FriendsProfilesListView(APIView):

    def get(self, request, *args, **kwargs):
        profiles = FriendsProfile.objects.all()
        content_type = ContentType.objects.get_for_model(FriendsProfile)
        photos = Photo.objects.filter(content_type=content_type)
        serializer = FriendsProfilesListSerializer(profiles, many=True, context={"photos": photos})
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
    pass
