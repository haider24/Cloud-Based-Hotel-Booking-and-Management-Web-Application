from django.db import models
from django.db.models.signals import pre_delete
from cloudinary.models import CloudinaryField
import cloudinary

# Create your models here.
from django.dispatch import receiver
from django.utils.safestring import mark_safe


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    email=models.EmailField()
    password=models.CharField(max_length=50)
    profilePicture=models.CharField(max_length=500)

    def __str__(self):
        return self.name


class RoomType(models.Model):
    type=models.CharField(max_length=100)
    def __str__(self):
        return self.type

class Room(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.ForeignKey(RoomType,on_delete=models.CASCADE)
    price= models.PositiveIntegerField()
    image1 = CloudinaryField('image',default=None,blank=True)
    image2 = CloudinaryField('image',default=None,blank=True)
    image3 = CloudinaryField('image',default=None,blank=True)
    image4 = CloudinaryField('image',default=None,blank=True)




    def __str__(self):
        return self.type

@receiver(pre_delete, sender=Room)
def photo_delete(sender, instance, **kwargs):
        cloudinary.uploader.destroy(instance.image1.public_id)
        cloudinary.uploader.destroy(instance.image2.public_id)
        cloudinary.uploader.destroy(instance.image3.public_id)
        cloudinary.uploader.destroy(instance.image4.public_id)



