import json

from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
from django.http import HttpResponse
from shop.models import StoreOwner, User


class StoreOwnerView(View):
    @staticmethod
    def data_status(data):
        return HttpResponse(
            json.dumps({"data": data, "status": "ok"}),
            content_type="application/json"
        )

    @staticmethod
    def failed_status(status):
        return HttpResponse(
            json.dumps({'status': status}),
            status=404,
            content_type="application/json")

    @staticmethod
    def ok_status():
        return HttpResponse(
            json.dumps({"status": "ok"}),
            status=200,
            content_type="application/json"
        )

    def get(self, request):
        owners = StoreOwner.objects.all()
        data = []
        for owner in owners:
            data.append(({'id': owner.id, 'user': str(owner.user), 'avatar': str(owner.avatar),
                          'registrated_at': str(owner.registrated_at)}))
        return StoreOwnerView.data_status(data)

    def post(self, request):
        data = json.loads(request.body)
        if 'id' in data and 'avatar' in data:
            owner = StoreOwner.objects.create(
                user=User.objects.get(id=data['id']),
                avatar=data['avatar']
            )
        elif 'id' in data:
            # print(type(User.objects.get(id=data['id'])))
            owner = StoreOwner.objects.create(
                user=User.objects.get(id=data['id'])
            )
        else:
            return StoreOwnerView.failed_status("invalid_post_data")
        owner.save()
        return self.ok_status()

    @staticmethod
    def check_view(request, id):
        if request.method == "GET":
            return StoreOwnerView.get_single(request, id)
        if request.method == "DELETE":
            return StoreOwnerView.delete(request, id)
        if request.method == "PATCH":
            return StoreOwnerView.edit(request, id)

    @staticmethod
    def get_single(request, id):
        try:
            owner = StoreOwner.objects.get(id=id)
        except ObjectDoesNotExist:
            return StoreOwnerView.failed_status("object_not_found")
        return StoreOwnerView.data_status(
            {"id": owner.id, "user": str(owner.user), "avatar": str(owner.avatar),
             'registrated_at': str(owner.registrated_at)})

    @staticmethod
    def delete(request, id):
        try:
            owner = StoreOwner.objects.get(id=id)
        except ObjectDoesNotExist:
            return StoreOwnerView.failed_status("object_not_found")
        owner.delete()
        return StoreOwnerView.ok_status()

    @staticmethod
    def edit(request, ID):
        data = json.loads(request.body)
        try:
            owner = StoreOwner.objects.get(id=ID)
        except ObjectDoesNotExist:
            return StoreOwnerView.failed_status("obj_not_found")
        if "id" in data:
            owner.user = User.objects.get(id=data["id"])
        if "avatar" in data:
            owner.avatar = data["avatar"]
        owner.save()
        return StoreOwnerView.ok_status()
