from django.contrib.auth import authenticate

from app.models import Verification, User
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
from django.http import HttpResponse
import json
from .functions import *


from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
class LoginView(View):

    def post(self, request):
        data = json.loads(request.body)
        try:
            email = data['email']
            password = data['password']
        except KeyError:
            return failed_status("missed field")
        user = authenticate(username=email, password=password)
        if user:
            try:
                user = User.objects.get(user=user)
                # apk = ApiKey.objects.get(user=user)
            except ObjectDoesNotExist:
                return failed_status("object doesn't exist")
        else:
            try:
                User.objects.get(email=email)
            except ObjectDoesNotExist:
                return failed_status("wrong email")
        return failed_status("wrong password")
