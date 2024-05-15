from django.db import models

# Create your models here.

class Inventory(models.Model):
    brand = models.CharField(max_length=60)
    type = models.CharField(max_length=60)
    productName = models.CharField(max_length=60, unique=True)
    desc = models.TextField()
    price = models.IntegerField()
    quantity = models.IntegerField()

    def __str__(self):
        return self.productName
    
    class Meta:
        verbose_name_plural = 'Inventory'