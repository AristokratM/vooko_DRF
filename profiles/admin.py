from django.contrib import admin
from .models import Interest, Nationality, Profile, Photo, AcquaintanceRequestType, AcquaintanceRequest, Match
# Register your models here.
admin.site.register(Interest)
admin.site.register(Nationality)
admin.site.register(Profile)
admin.site.register(Photo)
admin.site.register(AcquaintanceRequestType)
admin.site.register(AcquaintanceRequest)
admin.site.register(Match)
