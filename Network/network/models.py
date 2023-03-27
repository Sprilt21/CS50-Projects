from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    following = models.ManyToManyField("User", related_name='followage', blank=True, symmetrical= False)

    pass

class Post(models.Model):

    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField("Like", related_name="post_likes", blank=True)

    def serialize(self):
        
        return {
            'id': self.id,
            'user': self.user.username,
            'body': self.body,
            'timestamp': self.timestamp.strftime("%b %d %Y, %H:%M %p"),
            'likes': [like.user.username for like in self.likes.all()]
        }

class Like(models.Model):

    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="liked_by")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name='liked_post')