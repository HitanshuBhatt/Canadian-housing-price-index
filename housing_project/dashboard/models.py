from django.db import models

# model creted to store the housing data based on the csv uploaded
class HousingData(models.Model):
    # date of housing record 

    date = models.DateField()
    #  name of location
    geo = models.CharField(max_length=255)
    # name of category e.g. house 
    category = models.CharField(max_length=100)
    #  value of index 
    value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.geo} - {self.date}"