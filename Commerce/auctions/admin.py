from django.contrib import admin

from .models import Comment, Bid, Listing, User
# Register your models here.
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(Listing)
admin.site.register(User)