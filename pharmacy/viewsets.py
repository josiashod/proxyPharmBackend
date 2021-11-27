import datetime

from django.db.models.query_utils import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from xlib.utils import distance, get_client_ip

from .models import Drug, OnCallPharmacy, Pharmacy
from .serializers import DrugSerializer, LocateSerializer, PharmacySerializer


class PharmacyViewSet(viewsets.ModelViewSet):
    """
        Pharmacy viewSet
    """
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacySerializer
    permission_classes= []
    lookup_field = 'pk'
    lookup_value_regex = '[0-9]*'

    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many= True)
        # serializer_deleted =  self.get_serializer(Pharmacy.objects.deleted_only(), many= True)

        return Response({
            'data': serializer.data,
            # 'trashed_data': serializer_deleted.data
        })

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
    # loc = LocateSerializer(data=request.GET)
    # loc.is_valid(raise_exception=True)
    # lat = loc.validated_data['lat']
    # lng = loc.validated_data['lng']
    lat = 6.380182
    lng = 2.4441915

    pharmacies = PharmacySerializer(Pharmacy.objects.all(), many= True, context={'coord': {'lat': lat, 'lng': lng}}).data
    pharmacies.sort(key= lambda p: p['distance'])

    #returning all the ten oncallpharmcies who are nearest 
    now = datetime.datetime.now(datetime.timezone.utc)
    on_call_pharmacies = OnCallPharmacy.objects.filter(Q(end_at__gte= now) & Q(start_at__lte= now))
    on_call_pharmacies = list(map(lambda p: p.pharmacy, on_call_pharmacies))
    on_call_pharmacies = PharmacySerializer(on_call_pharmacies, many= True, context={'coord': {'lat': lat, 'lng': lng}}).data
    on_call_pharmacies.sort(key= lambda p: p['distance'])

    return Response({
        'data': {
            'pharmacies': pharmacies[0:10],
            'on_call_pharmacies': on_call_pharmacies[0:10]
        }
    })

@api_view(['GET'])
def search_pharmacies(request):
    # loc = LocateSerializer(data=request.GET)
    # loc.is_valid(raise_exception=True)
    # lat = loc.validated_data['lat']
    # lng = loc.validated_data['lng']
    lat = 6.380182
    lng = 2.4441915

    if 'q' not in request.GET.keys():
        return Response({'q':['This field is required']},status= 400)
    q = request.GET.get('q')
    if len(q) == 0:
        return Response({'q':['This field is required']},status= 400)

    
    pharmacies = PharmacySerializer(Pharmacy.objects.filter(name__icontains= q), many= True, context={'coord': {'lat': lat, 'lng': lng}}).data
    pharmacies.sort(key= lambda p: p['distance'])

    return Response({
        'data': pharmacies
    })

@api_view(['POST'])
def search_drug(request):
    drug = DrugSerializer(data= request.data)
    drug.is_valid(raise_exception= True)
    drugs = DrugSerializer(Drug.objects.filter(name__icontains= drug.data['name']), many= True).data
    return Response({
        'data': drugs
    })

def find_pharmacy_by_prescription(request):

    return Response()