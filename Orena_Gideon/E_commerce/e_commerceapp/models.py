from django.db import models

# Create your models here.

# Model for an E-commerce application.
class Product(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    category = models.CharField(max_length=255, null=False, blank=False)
    price = models.IntegerField(null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)
    color = models.CharField(max_length=255, null=False, blank=False)
    image = models.ImageField(upload_to='static/media/', null=False, blank=False)


    # Calling the model by its name.
    def __str__(self):
        return self.name


