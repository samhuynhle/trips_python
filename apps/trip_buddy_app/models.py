from django.db import models
from apps.login_registration_app.models import *
from time import localtime, strftime, strptime
from datetime import date, datetime

# Create your models here.
class TripManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}

        if len(postData['destination']) < 3:
            errors['destination'] = "Trip 'destination' must be longer than 3 characters"
        if postData['start_date'] < strftime("%Y-%m-%d", localtime()):
            errors['start_date'] = "Trip 'start date' invalid. You can't time travel to the past!"
        if postData['end_date'] < postData['start_date']:
            errors['end_date'] = "Trip 'end_date' invalid. End date must be after start date!"
        if len(postData['plan']) < 3:
            errors['plan'] = "Trip 'plan' must be longer than 3 characters"

        return errors


class Trip(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, related_name="creator")
    travelers = models.ManyToManyField(User, related_name="travelers")
    objects = TripManager()

    def __repr__(self):
        return f"<Trip object: {self.id}>"