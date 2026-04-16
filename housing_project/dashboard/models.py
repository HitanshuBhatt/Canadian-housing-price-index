from django.db import models


class HousingData(models.Model):
    date = models.CharField(max_length=20)
    geo = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    value = models.FloatField()

    def __str__(self):
        return f"{self.geo} - {self.date}"