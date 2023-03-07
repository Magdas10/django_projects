from app.models import Verification, User
from django.views.generic import View
from .functions import *


class RegisterView(View):

    def post(self, request):
        data = json.loads(request.body)
        if 'username' in data and 'email' in data and 'password' in data and 'first_name' in data and 'last_name' in data:
            if is_valid_email(data['email']):
                if User.objects.filter(email=data['email']).exists():
                    return HttpResponse(
                        json.dumps(
                            {
                                "status": "error",
                                "error": {
                                    "code": 1,
                                    "text": "An existing user is already registered with the given email address.",
                                },
                            }
                        ),
                        status=200,
                        content_type="application/json",
                    )
                user = User.objects.create_user(username=data['username'], email=data['email'],
                                                password=data['password'])
                user.first_name = data['first_name']
                user.last_name = data['last_name']
                user.is_active = True
                user.save()
                ver = Verification.objects.create(
                    user=user,
                    verification_code=hash(user.username)
                )
            else:
                return failed_status("invalid_post_data")
            ver.save()
            return ok_status()
        else:
            return failed_status("invalid_post_data")
