from django.contrib import admin
from .models import *


class VerificationAdmin(admin.ModelAdmin):
    # def verification(self, obj):
    #     obj.verification_code = hash(obj.user.username)
    #     obj.save()
    #     return obj.verification_code

    list_display = ('id', 'user', 'verification_code')


admin.site.register(Verification, VerificationAdmin)
