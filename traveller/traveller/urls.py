from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('main.urls')),
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('realadmin/', admin.site.urls),
]
