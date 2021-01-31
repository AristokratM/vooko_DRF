from django.urls import path
from .views import (
    FriendsProfilesListView,
    PhotoListView,
    PhotoDetailView,
    NatinalityDetailView,
    NationalitiesListView
)

urlpatterns = [
    path('profiles/', FriendsProfilesListView.as_view(), ),
    path('photos/', PhotoListView.as_view(), ),
    path('photo/', PhotoDetailView.as_view(), ),
    path('photo/<int:pk>', PhotoDetailView.as_view(), ),
    path('nationalities/', NationalitiesListView.as_view(), ),
    path('nationality/', NatinalityDetailView.as_view(), ),
    path('nationality/<int:pk>', NatinalityDetailView.as_view(), ),

]
