from django.db import models

class LostItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_lost = models.DateField()
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class FoundItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_found = models.DateField()
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.title
from django.db import models

# Create your models here.
