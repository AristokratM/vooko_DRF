from django.urls import path
from .views import (
    PhotoListView,
    PhotoDetailView,
    NationalityDetailView,
    NationalitiesListView,
    AcquaintanceRequestsListView,
    AcquaintanceRequestDetailView,
    MatchDetailView,
    MatchesListView,
    SexualOrientationDetailView,
    SexualOrientationsListView,
    ProfilesListView,
    ProfileDetailView,
    UserProfilesList,
)

urlpatterns = [
    path('photos/', PhotoListView.as_view(), name="photo-list"),
    path('photos/<int:pk>', PhotoDetailView.as_view(), name="photo-detail"),
    path('nationalities/', NationalitiesListView.as_view(), name="nationality-list"),
    path('nationalities/<int:pk>', NationalityDetailView.as_view(), name="nationality-detail"),
    path('acquaintanceRequests/', AcquaintanceRequestsListView.as_view(), name="acquaintanceRequest-list"),
    path('acquaintanceRequests/<int:pk>', AcquaintanceRequestDetailView.as_view(), name="acquaintanceRequest-detail"),
    path('matches/', MatchesListView.as_view(), name="match-list"),
    path('matches/<int:pk>', MatchDetailView.as_view(), name="match-detail"),
    path('sexualOrientations/', SexualOrientationsListView.as_view(), name="sexualOrientation-list"),
    path('sexualOrientations/<int:pk>', SexualOrientationDetailView.as_view(), name="sexualOrientation-detail"),
    path('profiles/', UserProfilesList.as_view(), name='user-profiles'),
    path('profiles/<int:ct_type>/', ProfilesListView.as_view(), name='profile-list'),
    path('profiles/<int:ct_type>/<int:pk>', ProfileDetailView.as_view(), name='profile-list'),

]
