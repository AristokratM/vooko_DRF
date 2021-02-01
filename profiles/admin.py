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
@admin.register(FriendsProfile)
class FriendsProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_active', 'user')
    ordering = ('id', )


admin.site.register(Interest)
admin.site.register(Nationality)
admin.site.register(DatesProfile)
admin.site.register(Photo)
admin.site.register(SexualOrientation)
admin.site.register(AcquaintanceRequest)
admin.site.register(Match)
