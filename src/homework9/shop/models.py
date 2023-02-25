from django.db import models
from django.contrib.auth.models import User


class StoreCategory(models.Model):
    name = models.CharField(max_length=200)
    picture = models.ImageField(upload_to='', blank=True)


class ItemCategory(models.Model):
    name = models.CharField(max_length=200)
    picture = models.ImageField(upload_to='', blank=True)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='', blank=True)
    registrated_at = models.DateTimeField(auto_now_add=True)


class StoreOwner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='', blank=True)
    registrated_at = models.DateTimeField(auto_now_add=True)


class Store(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(StoreOwner, on_delete=models.CASCADE)
    store_category = models.ForeignKey(StoreCategory, on_delete=models.PROTECT)


class Item(models.Model):
    name = models.CharField(max_length=200)
    picture = models.ImageField(upload_to='', blank=True)
    category = models.ForeignKey(ItemCategory, on_delete=models.PROTECT)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    info = models.TextField(default="lala")
    store = models.ForeignKey(Store, on_delete=models.CASCADE)


class MyBag(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)
    total_price = models.PositiveIntegerField(default=0, editable=False)

    def total(self):
        self.total_price = sum([item.price for item in self.items.all()])
        self.save()

    # total_price = sum(item["price"]*item['quantity'] for item in Item.objects.filter(name='item1'))


class Purchase(models.Model):
    items = models.ManyToManyField(Item)
    buy_time = models.DateTimeField(auto_now_add=True)
    # total_price = models.PositiveIntegerField(default=0, editable=False)

    @property
    def total_price(self):
        return sum([item.price for item in self.items.all()])
        # self.save()

    def quantity(self):
        for item in self.items.all():
            if item.quantity > 0:
                item.quantity -= 1
                item.save()
            else:
                self.items.remove(item)
                self.save()
        self.save()
