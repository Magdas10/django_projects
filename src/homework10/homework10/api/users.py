from django.views.generic import View
from app.serializers.verification import UserSerializer, User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets


class UserViewSet(viewsets.ModelViewSet):
    @api_view(['GET'])
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
