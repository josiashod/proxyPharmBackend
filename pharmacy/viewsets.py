import datetime
import copy

from django.db.models.query_utils import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
# from xlib.utils import distance


from .models import Drug, OnCallPharmacy, Pharmacy, PharmacyDrug
from .serializers import DrugSerializer, LocateSerializer, FindPharmaciesByDrugsSerializer, PharmacySerializer, SearchDrugByPharmacySerializer


class PharmacyViewSet(viewsets.ModelViewSet):
    """
        Pharmacy viewSet
    """
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacySerializer
    permission_classes= []
    lookup_field = 'pk'
    lookup_value_regex = '[0-9]*'

    # def list(self, request):
    #     serializer = self.get_serializer(self.get_queryset(), many= True)
    #     # serializer_deleted =  self.get_serializer(Pharmacy.objects.deleted_only(), many= True)

    #     return Response({
    #         'data': serializer.data,
    #         # 'trashed_data': serializer_deleted.data
    #     })

    # def create(self, request):
    #     pass

    # def retrieve(self, request, pk=None):
    #     pass

    # def update(self, request, pk=None):
    #     pass

    # def destroy(self, request, pk=None):
    #     pass

    # @action(detail= True, methods=['get'])
    # def restore(self, request, pk):
    #     p = Pharmacy.objects.filter(pk= pk).undelete(True)
    #     serializer = self.get_serializer(p, many=True)
    #     return Response(serializer.data)
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        # if self.action in ['list', 'create', 'update', 'partial_update', 'destroy']:
        #     permission_classes = [IsAuthenticated, IsAdminUser]
        # else:
        permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

@api_view(['GET'])
def find_nearest_pharmacies(request):
    loc = LocateSerializer(data=request.GET)
    loc.is_valid(raise_exception=True)
    lat = loc.validated_data['lat']
    lng = loc.validated_data['lng']
    # lat = 6.380182
    # lng = 2.4441915

    phar = Pharmacy.objects.raw(f'''
        SELECT *, ( 3959 * acos( cos( radians({str(lat)}) ) * cos( radians( latitude ) ) * cos( radians(longitude) - radians({str(lng)}) ) + sin( radians({str(lat)}) ) * sin( radians(latitude)))) AS distance
        from pharmacy_pharmacy
        ORDER BY distance 
        LIMIT 0
        OFFSET 20
    ''')
    pharmacies = PharmacySerializer(phar, many= True, context={'coord': {'lat': lat, 'lng': lng}}).data
    pharmacies.sort(key= lambda p: p['distance'])

    #returning all the ten oncallpharmcies who are nearest 
    now = datetime.datetime.now(datetime.timezone.utc)
    on_call_pharmacies = OnCallPharmacy.objects.filter(Q(end_at__gte= now) & Q(start_at__lte= now)).values_list('pharmacy', flat= True)
    on_call_pharmacies = PharmacySerializer(Pharmacy.objects.filter(id__in= on_call_pharmacies), many= True, context={'coord': {'lat': lat, 'lng': lng}}).data
    on_call_pharmacies.sort(key= lambda p: p['distance'])

    return Response({
        'data': {
            'pharmacies': pharmacies[0:10],
            'on_call_pharmacies': on_call_pharmacies[0:10]
        }
    })

@api_view(['GET'])
def search_pharmacies(request):
    loc = LocateSerializer(data=request.GET)
    loc.is_valid(raise_exception=True)
    lat = loc.validated_data['lat']
    lng = loc.validated_data['lng']
    # lat = 6.380182
    # lng = 2.4441915

    if 'q' not in request.GET.keys():
        return Response({'q':['This field is required']},status= 400)
    q = request.GET.get('q')
    if len(q) == 0:
        return Response({'q':['This field is required']},status= 400)

    # paginating pharmacie
    paginator = PageNumberPagination()
    paginate_pharmacies = paginator.paginate_queryset(Pharmacy.objects.filter(name__icontains= q), request)

    pharmacies = PharmacySerializer(paginate_pharmacies, many= True, context={'coord': {'lat': lat, 'lng': lng}}).data
    pharmacies.sort(key= lambda p: p['distance'])

    return paginator.get_paginated_response(pharmacies) 
    # Response({
    #     'data': pharmacies
    # })

@api_view(['GET'])
def search_drug_by_pharmacy(request, id):
    data = copy.copy(request.GET)
    data['pharmacy_id'] = id
    data = SearchDrugByPharmacySerializer(data= data)
    data.is_valid(raise_exception= True)

    paginator = PageNumberPagination()
    paginate_drugs = paginator.paginate_queryset(PharmacyDrug.objects.filter(pharmacy__id= data.validated_data['pharmacy_id'], drug__name__icontains= data.validated_data['q']), request)

    drugs = map(lambda p: p.drug, paginate_drugs)

    drugs = DrugSerializer(drugs, many= True, context={ 'pharmacy': data.validated_data['pharmacy_id'] }).data

    return paginator.get_paginated_response(drugs)

    # return Response({
    #     'data': drugs
    # })

@api_view(['POST'])
def find_pharmacy_by_drugs(request):
    # verify if coordinates are provided
    loc = LocateSerializer(data=request.GET)
    loc.is_valid(raise_exception=True)
    lat = loc.validated_data['lat']
    lng = loc.validated_data['lng']

    # if 'drugs' not in request.data.keys():
    drugs = FindPharmaciesByDrugsSerializer(data= request.data)
    drugs.is_valid(raise_exception=True)

    drugs = list(map(lambda d: d.get('name'), drugs.validated_data['drugs']))
    pharmacies = Pharmacy.objects.filter(drugs__name__in= drugs).distinct()
    pharmacies = PharmacySerializer(pharmacies, many= True, context={'coord': {'lat': lat, 'lng': lng}}).data
    pharmacies.sort(key= lambda p: p['distance'])

    now = datetime.datetime.now(datetime.timezone.utc)
    on_call_pharmacies = OnCallPharmacy.objects.filter(Q(end_at__gte= now) & Q(start_at__lte= now)).filter(pharmacy__drugs__name__in= drugs).values_list('pharmacy', flat= True)
    on_call_pharmacies = PharmacySerializer(Pharmacy.objects.filter(id__in= on_call_pharmacies), many= True, context={'coord': {'lat': lat, 'lng': lng}}).data
    on_call_pharmacies.sort(key= lambda p: p['distance'])

    return Response({
        'data': {
            'pharmacies': pharmacies[0:10],
            'on_call_pharmacies': on_call_pharmacies[0:10]
        }
    })


class DrugViewSet(viewsets.ModelViewSet):
    """
        Drug viewSet
    """
    queryset = Drug.objects.all()
    serializer_class = DrugSerializer
    permission_classes= []
    lookup_field = 'pk'
    lookup_value_regex = '[0-9]*'

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        # if self.action in ['list', 'create', 'update', 'partial_update', 'destroy']:
        #     permission_classes = [IsAuthenticated, IsAdminUser]
        # else:
        permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]


@api_view(['GET'])
def find_drug(request):
    if 'q' not in request.GET.keys():
        return Response({'q':['This field is required']},status= 400)
    q = request.GET.get('q')
    if len(q) == 0:
        return Response({'q':['This field is required']},status= 400)

    paginator = PageNumberPagination()
    paginate_drugs = paginator.paginate_queryset(Drug.objects.filter(name__icontains= q), request)

    drugs = DrugSerializer(paginate_drugs, many= True).data

    return paginator.get_paginated_response(drugs)