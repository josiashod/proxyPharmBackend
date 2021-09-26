from rest_framework import routers
from .viewsets import PharmacyViewSet, find_nearest_pharmacies
from django.urls import path
from rest_framework.routers import Route, DynamicRoute, SimpleRouter

router = routers.DefaultRouter()
router.register(r'pharmacies', PharmacyViewSet, basename='pharmacy.')

# urlpatterns = router.urls
urlpatterns = [
    *router.urls,
    path('pharmacies/nearest/', find_nearest_pharmacies, name="pharmacy.nearest")
]