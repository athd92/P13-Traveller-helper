from django.urls import path

from . import views

app_name = "main"  # here for namespacing of urls.

urlpatterns = [
    path("", views.index, name="index"),
    path("get_infos/", views.get_infos, name="get_infos"),
    path("login/", views.login_request, name="login"),
    path('logout/', views.logout_request, name="logout"),
    path('register/', views.register, name="register")
]
