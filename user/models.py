from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avg_rating = models.IntegerField(default=5)
    bio = models.TextField(blank=True, null=True)
    image_url = models.CharField(max_length=191, blank=True, null=True)

    def get_rating(self):
        return self.avg_rating / 2

    def get_full_stars(self):
        return self.avg_rating // 2

    def get_half_stars(self):
        return self.avg_rating % 2

    def get_empty_stars(self):
        return (10 - self.avg_rating) // 2


class Country(models.Model):
    class Meta:
        ordering = ['name']
    name = models.CharField(max_length=191)

    def __str__(self):
        return self.name


class Rating(models.Model):
    rater = models.ForeignKey(User, related_name='rater', on_delete=models.CASCADE)
    rated = models.ForeignKey(User, related_name='rated', on_delete=models.CASCADE)
    rating = models.IntegerField()


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=191)
    street_name = models.CharField(max_length=191)
    house_number = models.CharField(max_length=191)
    city = models.CharField(max_length=191)
    zip = models.CharField(max_length=191)

    def __str__(self):
        return f'{self.street_name} {self.house_number}, {self.zip} {self.city}. {self.country.name}'
