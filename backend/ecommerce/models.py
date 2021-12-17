from django.db import models

from users.models import User


class MyModelBase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Product(MyModelBase):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)
    image = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField(default=0)
    is_active = models.PositiveSmallIntegerField(default=1)


# table to store orders
class Order(MyModelBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=6, decimal_places=2)


# order items table
class OrderProducts(MyModelBase):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField()