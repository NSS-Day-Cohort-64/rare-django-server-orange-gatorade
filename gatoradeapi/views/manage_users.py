from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.db import IntegrityError
from django.core.exceptions import PermissionDenied
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from gatoradeapi.models import Author


@api_view(['PUT'])
def deactivate_user(request, pk=None):
    '''Allows admin to deactivate user account

    Method arguments:
      request -- The full HTTP request object, pk -- id of user to deactivate
    '''
    user_making_request = request.auth.user
    if user_making_request.is_staff:
        user_to_deactivate = get_object_or_404(Author, pk=pk)

        if user_to_deactivate.user.is_active == False:
            return Response({'message': 'That account has already been deactivated'}, status=status.HTTP_400_BAD_REQUEST)
    
        user_to_deactivate.user.is_active = False
        user_to_deactivate.user.save()
        user_to_deactivate.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'message': 'You must have admin permissions to deactivate users'}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['PUT'])
def activate_user(request, pk=None):
    '''Allows admin to reactivate user account

    Method arguments:
      request -- The full HTTP request object, pk -- id of user to reactivate
    '''
    user_making_request = request.auth.user
    if user_making_request.is_staff:
        user_to_activate = get_object_or_404(Author, pk=pk)

        if user_to_activate.user.is_active == True:
            return Response({'message': 'That account is already active'}, status=status.HTTP_400_BAD_REQUEST)
    
        user_to_activate.user.is_active = True
        user_to_activate.user.save()
        user_to_activate.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'message': 'You must have admin permissions to activate users'}, status=status.HTTP_401_UNAUTHORIZED)
    

