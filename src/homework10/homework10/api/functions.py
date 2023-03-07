from django.http import HttpResponse
import json
import re
import email.utils

def is_valid_email(email_str):
    regex_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(regex_pattern, email_str):
        return False

    try:
        email.utils.parseaddr(email_str)
    except ValueError:
        return False

    return True



def data_status(data):
    return HttpResponse(
        json.dumps({"data": data, "status": "ok"}),
        content_type="application/json"
    )


def failed_status(status):
    return HttpResponse(
        json.dumps({'status': status}),
        status=404,
        content_type="application/json")


def ok_status():
    return HttpResponse(
        json.dumps({"status": "ok"}),
        status=200,
        content_type="application/json"
    )
