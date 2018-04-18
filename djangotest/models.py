from django.db import models

# Create your models here.
class Customer(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=50)
    profilePicture=models.CharField(max_length=500)

    def __str__(self):
        return self.choice_text