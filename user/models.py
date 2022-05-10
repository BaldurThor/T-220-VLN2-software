from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver

from messaging.models import Message


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    avg_rating = models.IntegerField(default=5)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='users', blank=True)
    banner = models.ImageField(upload_to='users/banners', blank=True)

    def image_url(self):
        if self.image:
            return self.image.url
        else:
            return '/static/images/generic-profile.png'

    def banner_url(self):
        if self.banner:
            return self.banner.url
        else:
            return '/static/images/banner.jpg'

    def get_unread_messages(self):
        return Message.objects.filter(read_at=None, receiver=self.user).count()

    def calculate_avg_rating(self):
        aggr = Rating.objects.filter(rated=self.user).aggregate(avg_rating=Avg('rating'))
        if aggr['avg_rating']:
            self.avg_rating = aggr['avg_rating']
        else:
            self.avg_rating = 5


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

    def get_rating(self):
        return self.rating / 2


@receiver(post_save, sender=Rating)
def rating_saved(sender, instance, **kwargs):
    instance.rated.user_profile.calculate_avg_rating()
    instance.rated.user_profile.save()


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

