from django.contrib.auth.models import AbstractUser
from django.db import models

DEFAULT_ID = 1

class User(AbstractUser):
    won = []
    made = []
    watchlist = []

    pass

class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length = 300)
    startingBid = models.DecimalField(decimal_places=2, max_digits = 8)
    image = models.CharField(max_length=200,blank = True)
    category = models.CharField(max_length=64, blank = True)
    currentWinner = ""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    closed = False
    
    def __str__(self):
        return f"{self.title}/n{self.description}/n{self.startingBid}"

class Bid(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits = 8)
    def __str__(self):
        return f"{self.amount}"

class Comment(models.Model):
    comment = models.CharField(max_length = 300)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    def __str__(self):
        return self.comment
