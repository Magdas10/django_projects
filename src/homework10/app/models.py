from django.db import models
from django.contrib.auth.models import User


class Verification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=100, editable=False)
