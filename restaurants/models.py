from django.db import models

class Restaurant(models.Model):
    
    name = models.CharField(max_length=250)
    restro_id = models.IntegerField(unique=True)

    latitude = models.FloatField()
    longitude = models.FloatField()

    location = models.CharField(max_length=50)
    address = models.CharField(max_length=250)

    rating = models.FloatField(blank=True,null=True,help_text="Restaurant Rating")

    delivering_now = models.BooleanField(default=False)

    def get_map_url(self):
        map_url = f"https://maps.google.com/?q={self.latitude},{self.longitude}"
        return map_url
    
    def __str__(self):
        return self.name
    
