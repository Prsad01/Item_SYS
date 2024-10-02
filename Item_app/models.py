from django.db import models

# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=200,unique=True, blank=False, null=False)
    description = models.TextField(blank=True,null=True)
    quantity = models.IntegerField(null=False,default=0)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)