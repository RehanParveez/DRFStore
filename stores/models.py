from django.db import models

# Create your models here.
class Store(models.Model):
    name = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    owner = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name="stores")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=20)
    price = models.IntegerField()
    quantity = models.IntegerField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name