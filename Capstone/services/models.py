from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    pass

class Job(models.Model):

    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user")
    price = models.DecimalField(decimal_places=2,max_digits=10)
    postTime = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=1000)
    buyer = models.ForeignKey("User", on_delete=models.CASCADE, blank=True, null=True, related_name="buyer")

    def serialize(self):
        print(self.user.username)
        if self.buyer == None:
            return {
                "id" : self.id,
                "user" : self.user.username,
                "price" : self.price,
                "description" : self.description,
                "timestamp" : self.postTime.strftime("%D"),
                "buyer" : None
            }

        return {
            "id" : self.id,
            "user" : self.user.username,
            "price" : self.price,
            "description" : self.description,
            "timestamp" : self.postTime.strftime("%D"),
            "buyer" : self.buyer.username
        }

class Message(models.Model):

    sender = models.ForeignKey("User", on_delete=models.CASCADE, related_name="sender")
    text = models.CharField(max_length=800)
    receiver = models.ForeignKey("User", on_delete=models.CASCADE, related_name="receiver")
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):

        return {
            "id" : self.id,
            "sender" : self.sender.username,
            "receiver" : self.receiver.username,
            "text" : self.text,
            "timestamp" : self.timestamp.strftime("%b %d %Y, %H:%M %p")
        }