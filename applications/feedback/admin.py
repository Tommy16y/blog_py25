from django.contrib import admin
from applications.feedback.models import Like, Rating, Favorite
# Register your models here.


admin.site.register(Like)
admin.site.register(Rating)
admin.site.register(Favorite)