from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length= 255)

    def __str__(self):
        return self.name

class Product(models.Model):
    user = models.ForeignKey(User,null=True ,on_delete= models.CASCADE)
    name = models.CharField(max_length= 255)
    description = models.TextField(null= True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.CharField(max_length= 2083)
    category = models.ForeignKey(Category, on_delete= models.PROTECT)

    def __str__(self):
        return self.name

class Customers(models.Model):
    user = models.ForeignKey(User, null=True, on_delete= models.CASCADE)
    name = models.CharField(max_length= 255)
    adresse = models.CharField(max_length= 255)
    email = models.CharField(max_length= 255)
    company = models.CharField(max_length= 255)
    phone = models.IntegerField()
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    product = models.ForeignKey(Product, on_delete= models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.FloatField()
    total_price = models.FloatField()
    
    def __str__(self):
        return f'{self.quantity} of {self.product.name}'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    order_num = models.IntegerField()
    total_amount = models.FloatField()
    shipping_address = models.CharField(max_length= 255)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)

    def __str__(self):
        return f'Order No.{self.order_num}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete= models.CASCADE)
    product = models.ForeignKey(Product, on_delete= models.SET_NULL, null= True)
    quantity = models.PositiveIntegerField()
    unit_price = models.FloatField()
    total_price = models.FloatField()
    
    def __str__(self):
        return f'{self.quantity} of {self.product.name}'
