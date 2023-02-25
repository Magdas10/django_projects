import json
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
from django.http import HttpResponse
from shop.models import MyBag, Customer, Item


class MyBagView(View):
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
        my_bags = MyBag.objects.all()
        data = []
        for my_bag in my_bags:
            # my_bag.total_price = sum([item.price for item in my_bag.items.all()])
            # my_bag.total()
            data.append(({'id': my_bag.id, 'customer': str(my_bag.customer.user),
                          'items': ", ".join([item.name for item in my_bag.items.all()]),
                          'total_price': my_bag.total_price}))

        return MyBagView.data_status(data)

    def post(self, request):
        data = json.loads(request.body)
        if 'customer_id' in data and 'items_ids' in data:
            lst = Item.objects.filter(id__in=data['items_ids'])
            my_bag = MyBag.objects.create(
                customer=Customer.objects.get(id=data['customer_id']),
            )
            for item in lst:
                my_bag.items.add(item)
        else:
            return MyBagView.failed_status("invalid_post_data")
        my_bag.total()
        my_bag.save()
        return self.ok_status()

    @staticmethod
    def check_view(request, id):
        if request.method == "GET":
            return MyBagView.get_single(request, id)

        if request.method == "DELETE":
            return MyBagView.delete(request, id)
        if request.method == "PATCH":
            return MyBagView.edit(request, id)

    @staticmethod
    def get_single(request, id):
        try:
            my_bag = MyBag.objects.get(id=id)
        except ObjectDoesNotExist:
            return MyBagView.failed_status("object_not_found")
        return MyBagView.data_status({'id': my_bag.id, 'customer': str(my_bag.customer.user),
                                      'items': ", ".join([item.name for item in my_bag.items.all()]),
                                      'total_price': my_bag.total_price})

    @staticmethod
    def delete(request, id):
        try:
            category = MyBag.objects.get(id=id)
        except ObjectDoesNotExist:
            return MyBagView.failed_status("object_not_found")
        category.delete()
        return MyBagView.ok_status()

    @staticmethod
    def edit(request, id):
        data = json.loads(request.body)
        try:
            my_bag = MyBag.objects.get(id=id)
        except ObjectDoesNotExist:
            return MyBagView.failed_status("obj_not_found")
        if "customer_id" in data:
            my_bag.name = data['customer_id']
        my_bag.items.clear()
        lst = Item.objects.filter(id__in=data['items_ids'])
        if "items_ids" in data:
            for item in lst:
                my_bag.items.add(item)
        my_bag.total()
        my_bag.save()
        return MyBagView.ok_status()
