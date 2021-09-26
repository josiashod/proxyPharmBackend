from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from xlib.utils import mailer, send_message
from rest_framework.permissions import IsAuthenticated

from ..models import *
from .serializers import *

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    password_serializer = ChangePasswordSerializer(data= request.data)
    password_serializer.is_valid(raise_exception= True)
    user = request.user
    user.set_password(password_serializer.validated_data['password'])

    return Response({'message': 'Password changed successfully'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_info(request):
    info = UserInfoSerializer(data= request.data)
    info.is_valid(raise_exception= True)
    info.save()

    return Response({'message': 'Info changed successfully', 'data': info.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_email(request):
    email_serializer = ChangeEmailSerializer(data= request.data)
    email_serializer.is_valid(raise_exception= True)
    email_serializer.save()

    return Response({'message': 'Email changed successfully'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_phone(request):
    phone_serializer = ChangePhoneSerializer(data= request.data)
    phone_serializer.is_valid(raise_exception= True)
    phone_serializer.save()

    return Response({'message': 'Phone changed successfully'})

# def profile_picture(request):
#     if request.method == 'POST':
#         image = request.FILES['image']
#         user = request.user
#         user.profile_picture = image
#         user.save()
#         return Response({'message': 'Profile picture changed successfully'})

# def profile_picture_delete(request):
#     if request.method == 'POST':
#         user = request.user
#         user.profile_picture = None
#         user.save()
#         return Response({'message': 'Profile picture deleted successfully'})
