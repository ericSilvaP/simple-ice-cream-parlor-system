from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=65)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.FloatField()
    quantity_unit = models.CharField(max_length=65)
    cover = models.ImageField(
        upload_to="products/covers/%Y/%m/%d/", blank=True, default=""
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, default=None
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
