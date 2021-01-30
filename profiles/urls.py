from django.urls import path
from .views import ProfilesListView
urlpatterns = [
    path('profiles/', ProfilesListView.as_view())
]