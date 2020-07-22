from django.contrib import admin
from django.urls import include, path
# from django.conf.urls import handler404, handler500


urlpatterns = [
    path('', include('main.urls')),
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('realadmin/', admin.site.urls),
]

# handler404 = 'main.views.error_404_view'

# handler500 = 'main.views.error_500_view'
