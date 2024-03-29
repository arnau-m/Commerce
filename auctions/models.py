from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listings(models.Model):
    title = models.CharField(max_length=40, unique=True)
    price = models.IntegerField(default = 0)
    category = models.CharField(max_length=64)
    description = models.CharField(max_length=300)
    image = models.CharField(max_length=300)
    owner = models.CharField(max_length = 64 , default = 'SOME STRING')
    status = models.BooleanField(default = True)
    winner = models.CharField(max_length = 64 , blank = True)

    def __str__(self):
        return f"{self.title}"

class Bids(models.Model):
    username = models.CharField(max_length = 64, null= True)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)
    bid = models.IntegerField(default= 0)

    def __str__(self):
        return f"{self.username} bids for {self.listing}"

class Comments(models.Model):
    username = models.CharField(max_length=64, null= True)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, null= True)
    comment = models.TextField(max_length=200, null= True)

    def __str__(self):
        return f"({self.username} commented on {self.listing})"

class Watchlist(models.Model):
    username = models.CharField(max_length=64)
    listing = models.ForeignKey(Listings, on_delete = models.CASCADE,related_name = "listing")


    def get_title(self):
        return self.listing.title

    def __str__(self):
        return f"{self.username},{self.listing}"
