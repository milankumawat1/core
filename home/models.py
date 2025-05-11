from django.db import models

# Create your models here.
class Person(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)


class Product(models.Model):
   
    pass    # name = models.CharField(max_length=100)
    # price = models.DecimalField(max_digits=10, decimal_places=2)
    # description = models.TextField()
    # image = models.ImageField()
    # created_at = models.DateTimeField(auto_now_add=True)
    
    
