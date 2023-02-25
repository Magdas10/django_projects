import json
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
from django.http import HttpResponse
from shop.models import Purchase, Item


class PurchaseView(View):
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
        purchases = Purchase.objects.all()
        data = []
        for purchase in purchases:
            # purchase.total_price = sum([item.price for item in purchase.items.all()])
            # purchase.total()
            data.append(({'id': purchase.id, 'buy_time': str(purchase.buy_time),
                          'items': ", ".join([item.name for item in purchase.items.all()]),
                          'total_price': purchase.total_price}))

        return PurchaseView.data_status(data)

    def post(self, request):
        data = json.loads(request.body)
        if 'items_ids' in data:
            lst = Item.objects.filter(id__in=data['items_ids'])
            purchase = Purchase.objects.create()
            for item in lst:
                purchase.items.add(item)
        else:
            return PurchaseView.failed_status("invalid_post_data")
        purchase.quantity()
        # purchase.total()
        purchase.save()
        return self.ok_status()

    @staticmethod
    def check_view(request, id):
        if request.method == "GET":
            return PurchaseView.get_single(request, id)

        if request.method == "DELETE":
            return PurchaseView.delete(request, id)

        if request.method == "PATCH":
            return PurchaseView.edit(request, id)

    @staticmethod
    def get_single(request, id):
        try:
            purchase = Purchase.objects.get(id=id)
        except ObjectDoesNotExist:
            return PurchaseView.failed_status("object_not_found")
        return PurchaseView.data_status({'id': purchase.id, 'buy_time': str(purchase.buy_time),
                                         'items': ", ".join([item.name for item in purchase.items.all()]),
                                         'total_price': purchase.total_price})

    @staticmethod
    def delete(request, id):
        try:
            category = Purchase.objects.get(id=id)
        except ObjectDoesNotExist:
            return PurchaseView.failed_status("object_not_found")
        category.delete()
        return PurchaseView.ok_status()

    @staticmethod
    def edit(request, id):
        data = json.loads(request.body)
        try:
            purchase = Purchase.objects.get(id=id)
        except ObjectDoesNotExist:
            return PurchaseView.failed_status("obj_not_found")
        purchase.items.clear()
        lst = Item.objects.filter(id__in=data['items_ids'])
        if "items_ids" in data:
            for item in lst:
                purchase.items.add(item)
        purchase.quantity()
        purchase.total()
        purchase.save()
        return PurchaseView.ok_status()
