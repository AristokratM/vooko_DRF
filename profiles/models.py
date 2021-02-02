from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db import models
import os
from django.db.models.signals import post_save
from django.dispatch import receiver

PROFILES_MODELS = models.Q(app_label='profiles', model='friendsprofile') \
                  | models.Q(app_label='profiles', model='datesprofile')


class SexualOrientation(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Nationality(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Nationalities"

    def __str__(self):
        return self.name


class Match(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=PROFILES_MODELS)
    initiator_object_id = models.PositiveIntegerField()
    initiator = GenericForeignKey('content_type', 'initiator_object_id')

    confirmer_object_id = models.PositiveIntegerField()
    confirmer = GenericForeignKey('content_type', 'confirmer_object_id')
    match_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['content_type', 'initiator_object_id', 'confirmer_object_id'], name="profiles.Matches"
            )
        ]
        verbose_name_plural = "Matches"

    def __str__(self):
        return f"{self.content_type} ({self.initiator_object_id}, {self.confirmer_object_id})"


class AcquaintanceRequest(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=PROFILES_MODELS)
    sender_object_id = models.PositiveIntegerField()
    sender = GenericForeignKey('content_type', 'sender_object_id')

    receiver_object_id = models.PositiveIntegerField()
    receiver = GenericForeignKey('content_type', 'receiver_object_id')
    request_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['content_type', 'sender_object_id', 'receiver_object_id'], name="profiles.AcquaintanceRequests"
            )
        ]
        pass

    def __str__(self):
        return f"{self.content_type} ({self.sender_object_id}, {self.receiver_object_id})"


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
    nationality = models.ForeignKey(Nationality, on_delete=models.SET_NULL, null=True, blank=True)
    photos = GenericRelation('Photo', related_query_name="friends_profile")
    confirmed_matches = GenericRelation(
        'Match', related_query_name="friends_profile_confirmer", object_id_field='confirmer_object_id'
    )
    initiated_matches = GenericRelation(
        'Match', related_query_name="friends_profile_initiator", object_id_field='initiator_object_id'
    )

    sent_requests = GenericRelation(
        'AcquaintanceRequest', related_query_name="friends_profile_sender", object_id_field='sender_object_id'
    )
    received_requests = GenericRelation(
        'AcquaintanceRequest', related_query_name="friends_profile_receiver", object_id_field='receiver_object_id'
    )


class DatesProfile(BaseProfile):
    interests = models.ManyToManyField(Interest, related_name="%(app_label)s_%(class)s_related", null=True, blank=True)
    sexual_orientation = models.CharField(max_length=50, null=True, blank=True)
    photos = GenericRelation('Photo', related_query_name="dates_profile")
    initiated_matches = GenericRelation(
        'Match', related_query_name="dates_profile_initiator", object_id_field='initiator_object_id'
    )
    confirmed_matches = GenericRelation(
        'Match', related_query_name="dates_profile_confirmer", object_id_field='confirmer_object_id'
    )
    acquaintance_requests = GenericRelation(
        'AcquaintanceRequest', related_query_name="dates_profile_senders", object_id_field='sender_object_id'
    )
    received_requests = GenericRelation(
        'AcquaintanceRequest', related_query_name="dates_profile_receivers", object_id_field='receiver_object_id'
    )


@receiver(post_save, sender=Match)
def delete_acquaintance_request(sender, instance, created, **kwargs):
    if created:
        AcquaintanceRequest.objects.get(
            content_type=instance.content_type,
            sender_object_id=instance.initiator_object_id,
            receiver_object_id=instance.confirmer_object_id
        ).delete()


@receiver(post_save, sender=get_user_model())
def create_friend_profile(sender, instance, created, **kwargs):
    if created:
        fp = FriendsProfile.objects.create(user=instance)
        fp.is_active = True
        fp.save()


class Photo(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=PROFILES_MODELS)
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
