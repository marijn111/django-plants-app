from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Plant(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    age = models.DateTimeField(null=True)
    watering = models.IntegerField(null=True)
    standplace = models.CharField(max_length=20, null=True)
    image = models.ImageField(null=True, blank=True)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def __str__(self):
        return self.name


class Task(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant, null=True, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    date = models.DateField()

