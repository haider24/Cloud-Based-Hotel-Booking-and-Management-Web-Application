from django.db import models
from django.db.models.signals import pre_delete
from cloudinary.models import CloudinaryField
import cloudinary

# Create your models here.
from django.dispatch import receiver


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
    image1 = CloudinaryField('image',default=None)
    image2 = CloudinaryField('image',default=None)
    image3 = CloudinaryField('image',default=None)
    image4 = CloudinaryField('image',default=None)

    def __str__(self):
        return self.type

@receiver(pre_delete, sender=Room)
def photo_delete(sender, instance, **kwargs):
        cloudinary.uploader.destroy(instance.image1.public_id)
        cloudinary.uploader.destroy(instance.image2.public_id)
        cloudinary.uploader.destroy(instance.image3.public_id)
        cloudinary.uploader.destroy(instance.image4.public_id)