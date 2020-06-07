from django.contrib import admin
from main.models import Country, Post, Messages, UserAttributes

# Register your models here.
admin.site.register(Country)
admin.site.register(Post)
admin.site.register(Messages)
admin.site.register(UserAttributes)


