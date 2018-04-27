from django.db import models
from django.db.models.signals import pre_delete, post_save
from cloudinary.models import CloudinaryField
import cloudinary
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.dispatch import receiver
from django.utils.safestring import mark_safe
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, verbose_name='Rating', blank=True, null=True,validators=[MaxValueValidator(5), MinValueValidator(0)])
    profilePicture = CloudinaryField('image', default=None, blank=True, null=True)
    def name(self):
        return self.user.first_name
    def email(self):
        return self.user.email
    def Rating(self):
        return int(self.rating)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# class Customer(models.Model):
#     id = models.AutoField(primary_key=True)
#     name=models.CharField(max_length=100,verbose_name='Name')
#     email=models.EmailField(verbose_name='Email')
#     password=models.CharField(max_length=50,verbose_name='Password')
#     rating=models.IntegerField(default=0,verbose_name='Rating',blank=True,null=True,validators=[MaxValueValidator(5), MinValueValidator(0)])
#     profilePicture=CloudinaryField('image',default=None,blank=True,null=True)
#
#     def __str__(self):
#         return self.name


class RoomType(models.Model):
    id = models.AutoField(primary_key=True)
    type=models.CharField(max_length=100)
    price = models.PositiveIntegerField(validators=[MinValueValidator(1)],default=None)
    description=models.CharField(max_length=200,default=None)
    airConditioning = models.BooleanField(default=False, verbose_name='Air Conditioning')
    wifi = models.BooleanField(default=False, verbose_name='WiFi')
    roomService = models.BooleanField(default=False, verbose_name='Room Service')
    freeBreakfast = models.BooleanField(default=False, verbose_name='Free Breakfast')
    minibar = models.BooleanField(default=False, verbose_name='Mini Bar')
    laundaryService = models.BooleanField(default=False, verbose_name='Laundary Service')
    def __str__(self):
        return str(self.id)

class Image(models.Model):
    #id = models.AutoField(primary_key=True)
    roomType=models.ForeignKey(RoomType,on_delete=models.CASCADE,verbose_name='Room Type')
    image = CloudinaryField('image')
    def __str__(self):
        return self.image.url


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.ForeignKey(RoomType,on_delete=models.CASCADE,verbose_name='Room Type')
    def __str__(self):
        return str(self.type)
    def price(self):
        return self.type.price

class Booking(models.Model):
    room=models.ForeignKey(Room,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    start=models.DateField(verbose_name='From')
    end=models.DateField(verbose_name='To')
    bill=models.IntegerField(default=0,validators=[MinValueValidator(1)])



class Comment(models.Model):
    comment=models.CharField(max_length=200)
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=None)

    def _str_(self):
        return str(self.comment)

    def customername(self):
        return self.customer.first_name

    def customeremail(self):
        return self.customer.email
