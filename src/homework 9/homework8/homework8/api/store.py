import json

from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
from django.http import HttpResponse
from shop.models import Store, StoreOwner, StoreCategory


class StoreView(View):
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
        stores = Store.objects.all()
        data = []
        for store in stores:
            data.append(({'id': store.id, 'name': store.name, 'owner': str(store.owner.user),
                          'store_category': store.store_category.name}))
        return StoreView.data_status(data)

    def post(self, request):
        data = json.loads(request.body)
        if 'name' in data and 'owner_id' and 'store_category_id' in data:
            store = Store.objects.create(
                name=data['name'],
                owner=StoreOwner.objects.get(id=data['owner_id']),
                store_category=StoreCategory.objects.get(id=data['store_category_id'])
            )

        else:
            return StoreView.failed_status("invalid_post_data")
        store.save()
        return self.ok_status()

    @staticmethod
    def check_view(request, id):
        if request.method == "GET":
            return StoreView.get_single(request, id)
        if request.method == "DELETE":
            return StoreView.delete(request, id)
        if request.method == "PATCH":
            return StoreView.edit(request, id)

    @staticmethod
    def get_single(request, id):
        try:
            store = Store.objects.get(id=id)
        except ObjectDoesNotExist:
            return StoreView.failed_status("object_not_found")
        return StoreView.data_status(
            {"id": store.id, "name": store.name, "owner": str(store.owner.user),
             'store_category': store.store_category.name})

    @staticmethod
    def delete(request, id):
        try:
            owner = Store.objects.get(id=id)
        except ObjectDoesNotExist:
            return StoreView.failed_status("object_not_found")
        owner.delete()
        return StoreView.ok_status()

    @staticmethod
    def edit(request, ID):
        data = json.loads(request.body)
        try:
            store = Store.objects.get(id=ID)
        except ObjectDoesNotExist:
            return StoreView.failed_status("obj_not_found")
        if "name" in data:
            store.name = data["name"]
        if "owner_id" in data:
            store.owner = StoreOwner.objects.get(id=data["owner_id"])
        if "store_category_id" in data:
            store.store_category = data["store_category_id"]
        store.save()
        return StoreView.ok_status()
