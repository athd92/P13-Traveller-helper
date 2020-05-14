from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Trip(models.Model):
    """
    Class used to define a travel place
    """

    country = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    total_travelers = models.DecimalField(max_digits=4, decimal_places=0)
    wanted_travelers = models.DecimalField(max_digits=4, decimal_places=0)
    free_places = models.DecimalField(max_digits=4, decimal_places=0)
    interest = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    ready = models.BooleanField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __repr__(self):
        return f"{self.country} {self.city} {self.start_date} {self.end_date} {self.created_by}"


# Create your models here.
class Post(models.Model):
    """
    Class used to define a travel place
    """

    country = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    total_travelers = models.DecimalField(max_digits=4, decimal_places=0)
    wanted_travelers = models.DecimalField(max_digits=4, decimal_places=0)
    free_places = models.DecimalField(max_digits=4, decimal_places=0)
    interest = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    message = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    ready = models.BooleanField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __repr__(self):
        return f"{self.country} {self.city} {self.start_date} {self.end_date} {self.created_by}"


class Country(models.Model):
    """
    Class used to define a country
    """

    name = models.CharField(max_length=200)

    def __repr__(self):
        return self.name
