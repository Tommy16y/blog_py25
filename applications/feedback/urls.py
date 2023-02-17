from django.urls import path , include
from applications.feedback.views import FavoriteModelViewSet 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', FavoriteModelViewSet)

urlpatterns = [
    path('favorite/',include(router.urls)),

]
# urlspatterns += router.ulrs 