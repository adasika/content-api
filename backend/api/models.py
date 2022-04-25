from django.db import models
# Create your models here.


class News(models.Model):
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=2083, default="")
    published = models.DateTimeField()
    source = models.CharField(max_length=30, default="", blank=True, null=True)
    score = models.CharField(max_length=200, default="")