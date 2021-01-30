from django.contrib import admin
from .models import (
    Interest,
    Nationality,
    FriendsProfile,
    Photo,
    DatesProfile,
    AcquaintanceRequest,
    Match,
    SexualOrientation,
)
# Register your models here.
admin.site.register(Interest)
admin.site.register(Nationality)
admin.site.register(FriendsProfile)
admin.site.register(DatesProfile)
admin.site.register(Photo)
admin.site.register(SexualOrientation)
admin.site.register(AcquaintanceRequest)
admin.site.register(Match)
