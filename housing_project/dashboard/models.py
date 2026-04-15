from django.db import models

# Create your models here.
from django.db import models

class HousingData(models.Model):
    # DATE column (e.g., 2020-01-01)
    date = models.DateField()
    
    # GEO column (Geography/Location)
    geo = models.CharField(max_length=255)
    
    # CATEGORY column (e.g., house)
    category = models.CharField(max_length=100)
    
    # VALUE column (Housing price index)
    value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.geo} - {self.date} ({self.value})"