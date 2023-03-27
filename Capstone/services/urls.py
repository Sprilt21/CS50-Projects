from django.urls import path

from . import views

urlpatterns = [

    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("getCand", views.get_jobs, name="candidates"),
    path("getSenders", views.get_senders, name="senders"),
    path("getOlds", views.get_olds, name="old"),
    path("create", views.create_job, name="create"),
    path("hire/<int:job_id>", views.hire, name="hire"),
    path("getPMs/<str:other_user>", views.get_msgs, name="getPMs"),
    path("sendMsg/<str:other_user>", views.send_msg, name="sendMsg")
]
