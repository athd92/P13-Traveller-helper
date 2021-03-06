from django.urls import path
from . import views

app_name = "main"  # here for namespacing of urls.

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
    path("register/", views.register, name="register"),
    path("account/", views.account, name="account"),
    path("posts/", views.posts, name="posts"),
    path("send_post/", views.send_post, name="send_post"),
    path("delete_post/", views.delete_post, name="delete_post"),
    path("send_message/", views.send_message, name="send_message"),
    path("modify_post/", views.modify_post, name="modify_post"),
    path("upload_img/", views.upload_img, name="upload_img"),
    path("messages_posted/", views.messages_posted, name="messages_posted"),
    path("display_map/", views.display_map, name="display_map"),
    path('update_account/', views.update_account, name="update_account"),
    path("get_geocode/", views.get_geocode, name="get_geocode"),
    path("profil/", views.profil, name="profil"),
    path("delete_message/<int:message_id>/", views.delete_message, name="delete_message")
]


