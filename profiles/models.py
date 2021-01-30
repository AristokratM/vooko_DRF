from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
import os

from django.db.models.signals import post_save


class SexualOrientation(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Photo(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def get_upload_path(self, filename):
        return os.path.join(
            "photos", str(self.content_type.app_label) + "." + str(self.nice_content_type_name()),
            str(self.object_id), filename
        )

    photo = models.ImageField(upload_to=get_upload_path)

    def __str__(self):
        return f"{self.content_type.app_label}:{self.nice_content_type_name()}"

    def nice_content_type_name(self):
        return self.content_type.name.replace(" ", "_")


class Nationality(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Nationalities"

    def __str__(self):
        return self.name


class AcquaintanceRequest(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    sender_object_id = models.PositiveIntegerField()
    sender = GenericForeignKey('content_type', 'sender_object_id')

    receiver_object_id = models.PositiveIntegerField()
    receiver = GenericForeignKey('content_type', 'receiver_object_id')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['content_type', 'sender_object_id', 'receiver_object_id'], name="profiles.AcquaintanceRequests"
            )
        ]
        pass


class Match(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    initiator_object_id = models.PositiveIntegerField()
    initiator = GenericForeignKey('content_type', 'initiator_object_id')

    confirmer_object_id = models.PositiveIntegerField()
    confirmer = GenericForeignKey('content_type', 'confirmer_object_id')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['content_type', 'initiator_object_id', 'confirmer_object_id'], name="profiles.Matches"
            )
        ]
        verbose_name_plural = "Matches"

    def __str__(self):
        return f"{self.content_type} ({self.initiator_object_id}, {self.confirmer_object_id})"


class BaseProfile(models.Model):
    class Meta:
        abstract = True

    MAN = "M"
    WOMAN = "W"
    OTHER = "O"
    GENDER = [
        (MAN, "Man"),
        (WOMAN, "Woman"),
        (OTHER, "Other")
    ]
    sex = models.CharField(max_length=2, choices=GENDER, default=OTHER)
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=1000, null=True, blank=True)
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related"
    )
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.pk}:{self.user.first_name}"

    def get_age(self, birth_date):
        if birth_date == None:
            return None
        today = date.today()
        age = today.year - birth_date.year - 1
        if today.month > birth_date.month or (
                today.month == birth_date.month and today.day >= birth_date.day):
            age += 1
        return age


class Interest(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class FriendsProfile(BaseProfile):
    interests = models.ManyToManyField(Interest, related_name="%(app_label)s_%(class)s_related", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    nationality = models.ForeignKey(Nationality, on_delete=models.SET_NULL, null=True, blank=True)

    def create_friend_profile(sender, instance, created, **kwargs):
        if created:
            FriendsProfile.objects.create(user=instance)

    post_save.connect(create_friend_profile, sender=get_user_model())


class DatesProfile(BaseProfile):
    interests = models.ManyToManyField(Interest, related_name="%(app_label)s_%(class)s_related", null=True, blank=True)
    sexual_orientation = models.CharField(max_length=50, null=True, blank=True)
