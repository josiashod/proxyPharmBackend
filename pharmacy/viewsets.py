from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from .models import Pharmacy
from .serializers import PharmacySerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from xlib.utils import get_client_ip
import requests

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
    # ip = get_client_ip(request)
    # r = requests.get('https://ipinfo.io/' + ip +"?token=5b0b28296033b7")
    # 6.3654,2.4183
    return Response("6.3654,2.4183")