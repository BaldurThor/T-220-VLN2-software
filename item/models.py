from django.db import models
from django.contrib.auth.models import User
from django.utils.datetime_safe import date

from user.models import Country


class Condition(models.Model):
    name = models.CharField(max_length=191)

    def __str__(self):
        return f'#{self.id}: {self.name}'


class Category(models.Model):
    name = models.CharField(max_length=191)

    def __str__(self):
        return f'#{self.id}: {self.name}'

    class Meta:
        verbose_name_plural = 'categories'


class Item(models.Model):
    views = models.IntegerField(default=0)
    name = models.CharField(max_length=191)
    description = models.TextField()
    image_url = models.TextField()
    zip = models.CharField(max_length=191)
    sold_at = models.DateField(null=True, blank=True)
    published_at = models.DateField(default=date.today)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    condition = models.ForeignKey(Condition, on_delete=models.DO_NOTHING)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)
    seller = models.ForeignKey(User, related_name='item_seller', on_delete=models.DO_NOTHING)
    accepted_offer = models.ForeignKey('Offer', null=True, blank=True, on_delete=models.CASCADE, related_name='accepted_offer')
    categories = models.ManyToManyField(Category)


class Offer(models.Model):
    amount = models.IntegerField()
    date = models.DateField()
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Sale(models.Model):
    amount = models.IntegerField()
    full_name = models.CharField(max_length=191)
    street_name = models.CharField(max_length=191)
    house_number = models.CharField(max_length=191)
    city = models.CharField(max_length=191)
    zip = models.CharField(max_length=191)
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING)
    buyer = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='buyer')
    seller = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='seller')
    offer = models.ForeignKey(Offer, on_delete=models.DO_NOTHING)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)

    def fill_from_contact(self,):
        pass

    def fill_from_offer(self,):
        pass
