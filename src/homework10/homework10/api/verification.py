from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from app.serializers.verification import UserSerializer, User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
