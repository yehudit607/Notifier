from django.db import models

from datetime import datetime
from typing import Optional
from django.dispatch import Signal

from api.signals import notify_signal

ENTITY_TYPES = [
    "Event",
    "Company",
    "Webinar",
    "ContentItem",
    "CompanyForEvent",
    "CompanyForWebinar",
    "CompanyCompetitor"
]

CRAWLING_STATUSES = (
    (0, 'Not crawled'),
    (1, 'Error requesting link'),
    (2, 'Updating link'),
    (3, 'Marked as duplicate'),
    (4, 'Updated link'),
    (5, 'Crawling'),
    (6, 'Crawling failed'),
    (7, 'Rescheduled long crawling'),
    (8, 'Crawling too long'),
    (9, 'Has no pages'),
    (10, 'Text uploaded'),
    (11, 'Awaiting crawl'),
    (12, 'Indexed by elastic'),
    (13, 'Text analyzed'),
    (14, 'Domain invalid'),
    (15, 'No links in page'),
    (16, 'Uncrawlable')
)


class CrawlableEntity(models.Model):
    link = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=True)
    crawling_status = models.IntegerField(choices=CRAWLING_STATUSES, null=True)
    is_deleted = models.BooleanField(default=False, null=True)
    is_blacklisted = models.BooleanField(default=False, null=True)
    last_crawled = models.DateTimeField(null=True, )

    class Meta:
        app_label = 'api'

    def save(self, *args, **kwargs):
        # Get the original entity object before saving
        original_entity_obj = None
        if self.id:
            original_entity_obj = self.__class__.objects.filter(pk=self.id).first()
        super().save(*args, **kwargs)

        # Send the signal on save
        entity_type = self.__class__.__name__
        notify_signal.send(sender=self.__class__, entity_obj=self, original_entity_obj=original_entity_obj,
                           entity_type=entity_type)


class Event(CrawlableEntity):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True)
    description = models.TextField(null=True)
    location = models.CharField(max_length=255, null=True)

    @property
    def notify_on(self):
        return self

    class Meta:
        app_label = 'api'


class Webinar(CrawlableEntity):
    start_date = models.DateTimeField()
    description = models.TextField(null=True)
    language = models.CharField(max_length=2, default='en')

    @property
    def notify_on(self):
        return self

    class Meta:
        app_label = 'api'


class Company(CrawlableEntity):
    employees_min = models.IntegerField(null=True)
    employees_max = models.IntegerField(null=True)

    @property
    def notify_on(self):
        return self

    class Meta:
        app_label = 'api'


class ContentItem(CrawlableEntity):
    snippet = models.CharField(max_length=500, null=True, blank=True)
    company_content = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="company")

    @property
    def notify_on(self):
        return self.company_content

    class Meta:
        app_label = 'api'


class CompanyForEvent(CrawlableEntity):
    event_name = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="event_name", null=True)
    company_name = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="events",  null=True)

    @property
    def notify_on(self):
        return self.event_name

    class Meta:
        app_label = 'api'


class CompanyForWebinar(CrawlableEntity):
    webinar_name = models.ForeignKey(Webinar, on_delete=models.CASCADE, related_name="webinar_name",  null=True)
    company_name = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="webinars",  null=True)

    @property
    def notify_on(self):
        return self.webinar_name

    class Meta:
        app_label = 'api'

