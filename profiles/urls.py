from django.urls import path
from .views import (
    FriendsProfilesListView,
    PhotoListView,
    PhotoDetailView,
    NatinalityDetailView,
    NationalitiesListView,
    AcquaintanceRequestsListView,
    AcquaintanceRequestDetailView
)

urlpatterns = [
    path('profiles/', FriendsProfilesListView.as_view(), name="profiles-list"),
    path('photos/', PhotoListView.as_view(), name="photo-list"),
    path('photos/<int:pk>', PhotoDetailView.as_view(), name="photo-detail"),
    path('nationalities/', NationalitiesListView.as_view(), name="nationality-list"),
    path('nationalities/<int:pk>', NatinalityDetailView.as_view(), name="nationality-detail"),
    path('acquaintanceRequest/', AcquaintanceRequestsListView.as_view(), name="acquaintanceRequest-detail"),
    path('acquaintanceRequest/<int:pk>', AcquaintanceRequestDetailView.as_view(), name="acquaintanceRequest-detail"),

]
