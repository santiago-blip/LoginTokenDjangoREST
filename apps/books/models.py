from django.db import models

# Create your models here.
class Books(models.Model):
    title = models.CharField(max_length=30)
    author = models.CharField(max_length=30)

class Description(models.Model):
    description = models.CharField(max_length=30)
    book = models.ForeignKey(Books,on_delete=models.CASCADE)