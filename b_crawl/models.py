from django.db import models

class History(models.Model):
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255)