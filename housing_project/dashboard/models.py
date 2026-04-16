from django.db import models


class HousingData(models.Model):
    date = models.DateField()
    geo = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.geo} - {self.date}"