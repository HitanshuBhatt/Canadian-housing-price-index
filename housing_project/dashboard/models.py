from django.db import models
from django.contrib.auth.models import User


# model creted to store the housing data based on the csv uploaded
class HousingData(models.Model):
    # date of housing record
    date = models.DateField()

    # name of location
    geo = models.CharField(max_length=255)

    # name of category e.g. house
    category = models.CharField(max_length=100)

    # value of index
    value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.geo} - {self.date}"


# this model is for storing extra user info
# i added dob here because default django user model does not have date of birth
class UserProfile(models.Model):
    # linking one profile to one user
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # storing user's date of birth from signup form
    dob = models.DateField()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.user.email}"