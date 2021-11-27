from rest_framework import routers
from .viewsets import PharmacyViewSet, find_nearest_pharmacies, search_pharmacies, search_drug
from django.urls import path
from rest_framework.routers import Route, DynamicRoute, SimpleRouter

router = routers.DefaultRouter()
router.register(r'pharmacies', PharmacyViewSet, basename='pharmacy.')

# urlpatterns = router.urls
urlpatterns = [
    *router.urls,
    path('pharmacies/nearest/', find_nearest_pharmacies, name="pharmacy.nearest"),
    path('pharmacies/search/', search_pharmacies, name="pharmacy.search"),
    path('pharmacies/drug/search/', search_drug, name="pharmacy.drug.search")
]