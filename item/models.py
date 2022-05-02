from django.db import models
from django.contrib.auth.models import User
from user.models import Country


class Condition(models.Model):
    name = models.TextField()


class Item(models.Model):
    views = models.IntegerField()
    name = models.CharField(max_length=191)
    description = models.TextField()
    image_url = models.CharField(max_length=191)
    zip = models.CharField(max_length=191)
    sold_at = models.DateField(null=True)
    published_at = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    condition = models.ForeignKey(Condition, on_delete=models.DO_NOTHING)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)
    accepted_offer = models.ForeignKey('Offer', blank=True, on_delete=models.CASCADE, related_name='accepted_offer')


class Offer(models.Model):
    amount = models.IntegerField()
    date = models.DateField()
    accepted = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Category(models.Model):
    name = models.TextField()


class CategoryItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)


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
