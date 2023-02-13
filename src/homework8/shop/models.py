from django.db import models
from django.contrib.auth.models import User


class StoreCategory(models.Model):
    name = models.CharField(max_length=200)
    picture = models.ImageField(upload_to='')


class ItemCategory(models.Model):
    name = models.CharField(max_length=200)
    picture = models.ImageField(upload_to='', blank=True)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='', blank=True)
    registrated_at = models.DateTimeField(auto_now_add=True)


class StoreOwner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='')
    registrated_at = models.DateTimeField(auto_now_add=True)


class Store(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(StoreOwner, on_delete=models.CASCADE)
    store_category = models.ForeignKey(StoreCategory, on_delete=models.PROTECT)


class Item(models.Model):
    name = models.CharField(max_length=200)
    picture = models.ImageField(upload_to='')
    category = models.ForeignKey(ItemCategory, on_delete=models.PROTECT)
    price = models.PositiveIntegerField
    quantity = models.PositiveIntegerField
    info = models.TextField
    store = models.ForeignKey(Store, on_delete=models.PROTECT)


class MyBag(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)
    total_price = models.PositiveIntegerField


class Purchase(models.Model):
    items = models.ManyToManyField(Item)
    buy_time = models.DateTimeField(auto_now_add=True)
    total_price = models.PositiveIntegerField
