from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add", views.createListing, name="add"),
    path('listing/<str:name>', views.viewListing, name="item"),
    path('categories', views.categories, name="categories"),
    path('category/<str:category>', views.category, name="category"),
    path('bid/<str:name>', views.makeBid, name="bid"),
    path('watchlist', views.watchList, name="watchlist"),
    path('addWatchlist/<str:name>', views.addToWatch, name="addWatchlist"),
    path('close/<str:name>', views.close, name="close")
]
