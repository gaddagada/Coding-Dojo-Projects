from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
from datetime import datetime, time, date
from time import strftime

# Create your models here.

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# email validation - must follow standard email format
PW_REGEX = re.compile(r'(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}')
# password validation - must be at least 8 char, have 1 number, 1 lowercase, 1 uppercase


class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData["fname"]) < 2 or len(postData["lname"]) < 2:
            errors["name"] = "Both names must be at least 2 characters long."
        if not EMAIL_REGEX.match(postData["email"]):
            errors["email"] = "Invalid email address."
        if not len(postData["pw"]):
            errors["pw"] = "Passwords must be at least 8 characters long."
        if postData["pw"] != postData["conf_pw"]:
            errors["pw_match"] = "Passwords do not match!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    pw_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class TripManager(models.Manager):
    def trip_validator(self, postData):
        d = datetime.now()
        print("*******************")
        print(d)
        print("*******************")
        now=d.strftime("%Y-%m-%d")
        print("*******************")
        print(now)
        print("*******************")
        result = {
            'status' : False,
            'errors' : []
        }
        if len(postData["destination"]) < 2:
            result['errors'].append("Must enter a destination of at least two characters")
        if len(postData["plan"]) < 10:
            result['errors'].append("Must enter a description of at least ten characters")
        if len(postData["date_from"]) < 10:
            result['errors'].append("Must enter Travel Date From")
        if len(postData["date_to"]) < 10:
            result['errors'].append("Must enter Travel Date To")
        if postData["date_to"] < postData['date_from']:
            result['errors'].append("Can't return earlier than you leave")
        if postData["date_from"] < now:
            result['errors'].append("Please don't enter a date in the past")
        if len(result['errors']) < 1:
                result["status"] = True
        #     newtrip = Trip.objects.create(
        #         destination=postData['destination'], start_date=postData['date_from'], 
        #         end_date=postData['date_to'], 
        #         plan=postData['plan'],
        #         created_by=User.objects.get(id=postData['userid']))
        #     newtrip.trip_members.add(User.objects.get(id=postData['userid']))
        #     newtrip.save()
        return result

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.CharField(max_length=255)
    end_date = models.CharField(max_length=12)
    plan = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    trip_members = models.ManyToManyField(User, related_name="joined_trips" )
    created_by = models.ForeignKey(User, related_name="created_trips", on_delete="cascade")
    objects = TripManager()