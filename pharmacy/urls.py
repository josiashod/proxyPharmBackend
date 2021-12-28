from rest_framework import routers
from .viewsets import PharmacyViewSet, DrugViewSet, find_nearest_pharmacies, search_pharmacies, search_drug_by_pharmacy, find_drug, find_pharmacy_by_drugs
from django.urls import path
from rest_framework.routers import Route, DynamicRoute, SimpleRouter

router = routers.DefaultRouter()
router.register(r'pharmacies', PharmacyViewSet, basename='pharmacy.')
router.register(r'drugs', DrugViewSet, basename='drug.')

# urlpatterns = router.urls
urlpatterns = [
    *router.urls,
    path('pharmacies/nearest/', find_nearest_pharmacies, name="pharmacy.nearest"),
    path('pharmacies/search/', search_pharmacies, name="pharmacy.search"),
    path('pharmacies/search_by_drugs/', find_pharmacy_by_drugs, name="pharmacy.search_by_drugs"),
    path('pharmacies/<int:id>/drug/', search_drug_by_pharmacy, name="pharmacy.drug.search"),
    path('drugs/search/', find_drug, name="drug.search")
]