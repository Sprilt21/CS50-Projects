from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>/", views.entry, name="entry"),
    path("random", views.rng, name="rng"),
    path("add", views.add, name="add"),
    path("<str:title>/edit", views.edit, name="edit"),
    path("search", views.get_query, name="search")
]
