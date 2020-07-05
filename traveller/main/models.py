from django.db import models
from django.contrib.auth.models import User


class Country(models.Model):
    """
    Class used to define a country
    """

    name = models.CharField(max_length=200)
    alpha_2 = models.CharField(max_length=20)
    alpha_3 = models.CharField(max_length=20)
    temp_averges = models.CharField(max_length=500)
    flag = models.CharField(max_length=200)
    resume = models.TextField()
    picture = models.TextField()

    def __repr__(self):
        return f"{self.name} {self.alpha_2} {self.alpha_3}"


# Create your models here.
class Post(models.Model):
    """
    Class used to define a travel place
    """

    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    creation_date = models.DateField(auto_now=True)
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
    budget = models.CharField(max_length=100)

    def __repr__(self):
        return f"{self.country} {self.city} {self.start_date} {self.end_date} {self.created_by}"


class UserAttributes(models.Model):
    """
    Class used to edit the user profil attributes
    """

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=100)
    last_connexion = models.DateField()
    about = models.TextField()
    img = models.TextField()


class Messages(models.Model):
    """
    Class used to store messages send
    """

    title = models.CharField(max_length=200)
    created_at = models.DateField(auto_now=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
