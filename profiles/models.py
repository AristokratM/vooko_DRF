from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
import os
from datetime import date


class Interest(models.Model):
    """User interests"""
    name = models.CharField(verbose_name="Name", max_length=50)

    def __str__(self):
        return self.name


class Nationality(models.Model):
    class Meta:
        verbose_name_plural = "Nationalities"

    name = models.CharField("Nationality", max_length=100)

    def __str__(self):
        return self.name


class Profile(models.Model):
    """Model with all extra user data"""
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, verbose_name="User", related_name="profile")
    bio = models.TextField(max_length=1000, null=True, blank=True)
    matched = models.ManyToManyField('self', verbose_name="Matched", null=True, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    interests = models.ManyToManyField(
        Interest, verbose_name="Interests", related_name="user_profiles", null=True, blank=True
    )
    nationality = models.ForeignKey(Nationality, on_delete=models.CASCADE, related_name="profiles", null=True,
                                    blank=True)

    def __str__(self):
        return self.user.first_name

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    post_save.connect(create_user_profile, sender=get_user_model())

    def get_age(self):
        today = date.today()
        age = today.year - self.birth_date.year - 1
        if today.month > self.birth_date.month or (today.month == self.birth_date.month and today.day >= self.birth_date.day):
            age += 1
        return age


class Photo(models.Model):
    """User photos"""
    user_profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, verbose_name="User profile", related_name="photos"
    )

    def get_upload_path(self, filename):
        return os.path.join(
            'photos',
            str(self.user_profile.pk), filename
        )

    photo = models.ImageField("Photo", upload_to=get_upload_path)

    def __str__(self):
        return self.user_profile.user.first_name


class AcquaintanceRequestType(models.Model):
    name = models.CharField(verbose_name="Request Type", max_length=100)

    def __str__(self):
        return self.name


class Match(models.Model):
    initiator = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="matches_initiated")
    confirmer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="matches_confirmed")
    type = models.ForeignKey(
        AcquaintanceRequestType, on_delete=models.SET_NULL, related_name="matched", null=True, blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['initiator', 'confirmer'], name="profiles.Matches")
        ]
        verbose_name_plural = "Matches"


class AcquaintanceRequest(models.Model):
    """ First user - sender,
        Second user - receiver,
        Type - request type
    """
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="out_requests")
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="in_requests")
    type = models.ForeignKey(
        AcquaintanceRequestType, on_delete=models.SET_NULL, related_name="requests", null=True, blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['sender', 'receiver'], name="profiles.AcquaintanceRequests")
        ]

    def delete_request(sender, instance, created, **kwargs):
        if created:
            AcquaintanceRequest.objects.delete(sender=instance.user1, receiver=instance.user2)

    post_save.connect(delete_request, sender=Match)

    def __str__(self):
        return f"From {self.sender} to {self.receiver} ({self.type})"
