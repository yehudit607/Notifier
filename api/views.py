from django.shortcuts import render

from django.http import HttpResponse
from api.models import Company, CompanyForEvent, Event
from notifier_module.helpers.base_helpers import general_exception
from notifier_module.notifier import Notifier
import datetime


def test_notifier(request):
    try:
        company = Company(name='Test Company', is_deleted=False)
        company.save()
        company.is_deleted = True
        company.save()
        event = Event(start_date=datetime.datetime.now(), is_blacklisted=False)
        event.save()
        event.is_blacklisted = True
        event.save()
        company_for_event = CompanyForEvent(event_name=event, company_name=company)
        company_for_event.save()

        return HttpResponse("Test completed successfully!")

    except Exception as ex:
        return general_exception()

