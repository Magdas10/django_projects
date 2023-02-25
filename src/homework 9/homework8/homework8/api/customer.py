import json

from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
from django.http import HttpResponse
from shop.models import Customer, User


class CustomerView(View):
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
        customers = Customer.objects.all()
        data = []
        for customer in customers:
            data.append(({'id': customer.id, 'user': str(customer.user), 'avatar': str(customer.avatar),
                          'registrated_at': str(customer.registrated_at)}))
        return CustomerView.data_status(data)

    def post(self, request):
        data = json.loads(request.body)
        if 'id' in data:
            # print(type(User.objects.get(id=data['id'])))
            customer = Customer.objects.create(
                user=User.objects.get(id=data['id'])
            )
        else:
            return CustomerView.failed_status("invalid_post_data")
        customer.save()
        return self.ok_status()

    @staticmethod
    def check_view(request, id):
        if request.method == "GET":
            return CustomerView.get_single(request, id)
        if request.method == "DELETE":
            return CustomerView.delete(request, id)
        if request.method == "PATCH":
            return CustomerView.edit(request, id)

    @staticmethod
    def get_single(request, id):
        try:
            customer = Customer.objects.get(id=id)
        except ObjectDoesNotExist:
            return CustomerView.failed_status("object_not_found")
        return CustomerView.data_status(
            {"id": customer.id, "user": str(customer.user), "avatar": str(customer.avatar),
             'registrated_at': str(customer.registrated_at)})

    @staticmethod
    def delete(request, id):
        try:
            customer = Customer.objects.get(id=id)
        except ObjectDoesNotExist:
            return CustomerView.failed_status("object_not_found")
        customer.delete()
        return CustomerView.ok_status()

    @staticmethod
    def edit(request, ID):
        data = json.loads(request.body)
        try:
            customer = Customer.objects.get(id=ID)
        except ObjectDoesNotExist:
            return CustomerView.failed_status("obj_not_found")
        if "id" in data:
            customer.user = User.objects.get(id=data["id"])
        if "avatar" in data:
            customer.avatar = data["avatar"]
        customer.save()
        return CustomerView.ok_status()
