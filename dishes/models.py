from django.db import models
from restaurants.models import Restaurant

class Dish(models.Model):

    name = models.CharField(max_length=250)

    onwards = models.BooleanField(default=False)

    price = models.DecimalField(max_digits=6,decimal_places=2)

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="dishes"
        )

    def __str__(self):
        return self.name

