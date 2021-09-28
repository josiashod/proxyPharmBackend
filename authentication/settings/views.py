from copy import copy

from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import *
from .serializers import *


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    password_serializer = ChangePasswordSerializer(data= request.data, context={'request': request})
    password_serializer.is_valid(raise_exception= True)
    user = request.user
    user.set_password(password_serializer.validated_data['password'])

    return Response({'message': 'Password changed successfully'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_info(request):
    info = UserInfoSerializer(data= request.data, context={'request': request})
    info.is_valid(raise_exception= True)
    info.save()

    return Response({'message': 'Info changed successfully', 'data': info.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_email(request):
    email_serializer = ChangeEmailSerializer(data= request.data, context={'request': request})
    email_serializer.is_valid(raise_exception= True)
    email_serializer.save()

    return Response({'message': 'Email changed successfully'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_username(request):
    username_serializer = ChangeUsernameSerializer(data= request.data, context={'request': request})
    username_serializer.is_valid(raise_exception= True)
    username_serializer.save()

    return Response({'message': 'Username changed successfully'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_phone(request):
    phone_serializer = ChangePhoneSerializer(data= request.data, context={'request': request})
    phone_serializer.is_valid(raise_exception= True)
    phone_serializer.save()

    return Response({'message': 'Phone changed successfully'})

class ProfileImage(APIView):
    serializer_class = UploadImageFileSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data= request.data, context={'request': request})
        serializer.is_valid(raise_exception= True)
        serializer.save()
        return Response(str(request.user.person.image))


# def profile_picture_delete(request):
#     if request.method == 'POST':
#         user = request.user
#         user.profile_picture = None
#         user.save()
#         return Response({'message': 'Profile picture deleted successfully'})
