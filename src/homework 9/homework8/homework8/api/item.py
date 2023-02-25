import json

from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
from django.http import HttpResponse
from shop.models import Item, ItemCategory, Store


class ItemView(View):
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
        items = Item.objects.all()
        data = []
        for item in items:
            data.append(({'id': item.id, 'name': item.name, 'picture': str(item.picture),
                          'category': item.category.name, 'price': item.price, 'quantity': item.quantity,
                          'info': item.info, 'store': item.store.name}))
        return ItemView.data_status(data)

    def post(self, request):
        data = json.loads(request.body)
        if 'name' in data and 'category_id' in data and 'price' in data and 'quantity' in data and 'info' in data and 'store_id' in data:
            store = Item.objects.create(
                name=data['name'],
                category=ItemCategory.objects.get(id=data['category_id']),
                price=data['price'],
                quantity=data['quantity'],
                info=data['info'],
                store=Store.objects.get(id=data['store_id'])
            )

        else:
            return ItemView.failed_status("invalid_post_data")
        store.save()
        return self.ok_status()

    @staticmethod
    def check_view(request, id):
        if request.method == "GET":
            return ItemView.get_single(request, id)
        if request.method == "DELETE":
            return ItemView.delete(request, id)
        if request.method == "PATCH":
            return ItemView.edit(request, id)

    @staticmethod
    def get_single(request, id):
        try:
            item = Item.objects.get(id=id)
        except ObjectDoesNotExist:
            return ItemView.failed_status("object_not_found")
        return ItemView.data_status(
            {'id': item.id, 'name': item.name, 'picture': str(item.picture),
             'category': item.category.name, 'price': item.price, 'quantity': item.quantity,
             'info': item.info, 'store': item.store.name})

    @staticmethod
    def delete(request, id):
        try:
            item = Item.objects.get(id=id)
        except ObjectDoesNotExist:
            return ItemView.failed_status("object_not_found")
        item.delete()
        return ItemView.ok_status()

    @staticmethod
    def edit(request, ID):
        data = json.loads(request.body)
        try:
            item = Item.objects.get(id=ID)
        except ObjectDoesNotExist:
            return ItemView.failed_status("obj_not_found")
        if "name" in data:
            item.name = data["name"]
        if "picture" in data:
            item.picture = data["picture"]
        if "category_id" in data:
            item.category = ItemCategory.objects.get(id=data["category_id"])
        if "price" in data:
            item.price = data["price"]
        if "quantity" in data:
            item.quantity = data["quantity"]
        if "info" in data:
            item.info = data["info"]
        if "store_id" in data:
            item.store = Store.objects.get(id=data["store_id"])
        item.save()
        return ItemView.ok_status()
