from django.db import models



class Customers(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=50)
    profilePicture=models.CharField(max_length=500)

    def __unicode__(self):
        return self.content