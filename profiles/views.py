from django.shortcuts import render
from rest_framework.views import APIView
from .models import Profile
from .serializers import ProfilesListSerializer
from rest_framework.response import Response


# Create your views here.

class ProfilesListView(APIView):

    def get(self, request, *args, **kwargs):
        profiles = Profile.objects.all()
        serializer = ProfilesListSerializer(profiles, many=True)
        return Response(serializer.data)
