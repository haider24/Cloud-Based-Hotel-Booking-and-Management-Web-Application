from django.db import models
from django.db.models.signals import pre_delete
from cloudinary.models import CloudinaryField
import cloudinary
from django.core.validators import MinValueValidator


# Create your models here.
from django.dispatch import receiver
from django.utils.safestring import mark_safe
from django.core.validators import MaxValueValidator, MinValueValidator


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=100,verbose_name='Name')
    email=models.EmailField(verbose_name='Email')
    password=models.CharField(max_length=50,verbose_name='Password')
    rating=models.IntegerField(default=0,verbose_name='Rating',blank=True,null=True,validators=[MaxValueValidator(5), MinValueValidator(0)])
    profilePicture=CloudinaryField('image',default=None,blank=True,null=True)

    def __str__(self):
        return self.name


class RoomType(models.Model):
    type=models.CharField(max_length=100)
    def __str__(self):
        return self.type

class Image(models.Model):
    id = models.AutoField(primary_key=True)
    image = CloudinaryField('image', default=None, blank=True, null=True)
    def __str__(self):
        return self.image.url


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.ForeignKey(RoomType,on_delete=models.CASCADE)
    price= models.PositiveIntegerField(validators=[MinValueValidator(1)])
    images=models.ManyToManyField('Image',blank=True)
    # image1 = CloudinaryField('image',default=None,blank=True,null=True)
    # image2 = CloudinaryField('image',default=None,blank=True,null=True)
    # image3 = CloudinaryField('image',default=None,blank=True,null=True)
    # image4 = CloudinaryField('image',default=None,blank=True,null=True)
    def __str__(self):
        return str(self.type)





# @receiver(pre_delete, sender=Room)
# def photo_delete(sender, instance, **kwargs):
#         cloudinary.uploader.destroy(instance.image1.public_id)
#         cloudinary.uploader.destroy(instance.image2.public_id)
#         cloudinary.uploader.destroy(instance.image3.public_id)
#         cloudinary.uploader.destroy(instance.image4.public_id)



class Comment(models.Model):
    comment=models.CharField(max_length=200)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)

    def _str_(self):
        return str(self.comment)

    def customername(self):
        return self.customer.name

    def customeremail(self):
        return self.customer.email
