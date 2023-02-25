import json
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
from django.http import HttpResponse
from shop.models import StoreCategory


class StoreCategoryView(View):
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
        stores = StoreCategory.objects.all()
        data = []
        for store in stores:
            data.append(({'id': store.id, 'name': store.name}))
        return StoreCategoryView.data_status(data)

    def post(self, request):
        data = json.loads(request.body)
        if 'name' in data and 'picture' in data:
            category = StoreCategory.objects.create(
                name=data['name'],
                picture=data['picture']
            )
        elif 'name' in data:
            category = StoreCategory.objects.create(
                name=data['name']
            )
        elif 'picture' in data:
            category = StoreCategory.objects.create(
                picture=data['picture']
            )
        else:
            return StoreCategoryView.failed_status("invalid_post_data")
        category.save()
        return self.ok_status()

    @staticmethod
    def check_view(request, id):
        if request.method == "GET":
            return StoreCategoryView.get_single(request, id)
        if request.method == "DELETE":
            return StoreCategoryView.delete(request, id)
        if request.method == "PATCH":
            return StoreCategoryView.edit(request, id)

    @staticmethod
    def get_single(request, id):
        try:
            category = StoreCategory.objects.get(id=id)
        except ObjectDoesNotExist:
            return StoreCategoryView.failed_status("object_not_found")
        return StoreCategoryView.data_status({"id": category.id, "name": category.name})

    @staticmethod
    def delete(request, id):
        try:
            category = StoreCategory.objects.get(id=id)
        except ObjectDoesNotExist:
            return StoreCategoryView.failed_status("object_not_found")
        category.delete()
        return StoreCategoryView.ok_status()

    @staticmethod
    def edit(request, id):
        data = json.loads(request.body)
        try:
            category = StoreCategory.objects.get(id=id)
        except ObjectDoesNotExist:
            return StoreCategoryView.failed_status("obj_not_found")
        if "name" in data:
            category.name = data['name']
        if "picture" in data:
            category.picture = data['picture']
        category.save()
        return StoreCategoryView.ok_status()
