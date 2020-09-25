from django.db import models


# Create your models here.
class Plant(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    age = models.DateTimeField()

    def __str__(self):
        return self.name
