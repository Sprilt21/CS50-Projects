
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    #API urls
    path("posts", views.add, name="add"),
    path("posts/edit/<int:post_id>", views.edit, name="edit"),
    path("posts/like/<int:post_id>", views.like, name="like"),
    path("posts/unlike/<int:post_id>", views.unlike, name="unlike"),
    path("posts/follow/<str:profile>", views.follow, name="follow"),
    path("posts/unfollow/<str:profile>", views.unfollow, name="unfollow"),
    path("posts/isfollowing/<str:profile>", views.is_following, name="is_following"),
    path("posts/haveliked/<int:post_id>", views.have_liked),
    path("posts/<str:page>", views.viewpage, name="viewpage"),
    path("posts/get/<int:post_id>", views.get_post, name='get')
]
