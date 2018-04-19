from django.db import models

# Create your models here.
class Customer(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    password=models.CharField(max_length=50)
    profilePicture=models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Room(models.Model):
    type = models.CharField(max_length=100)
    price= models.IntegerField()
    image1 = models.ImageField()
    image2 = models.ImageField()
    image3 = models.ImageField()
    image4 = models.ImageField()

    def __str__(self):
        return self.type