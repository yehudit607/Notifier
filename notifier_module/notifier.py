from notifier_module.service import *
from django.dispatch import receiver
from api.signals import notify_signal
from notifier_module.helpers.constants import ActionType


class Notifier:
    @staticmethod
    @receiver(notify_signal)
    def handle_notification(sender, entity_obj, original_entity_obj, entity_type, **kwargs):
        if original_entity_obj is None:
            Notifier.handle_created(entity_type, entity_obj)
        elif entity_obj is None:
            Notifier.handle_deleted(entity_type, original_entity_obj)
        else:
            Notifier.handle_updated(entity_type, entity_obj, original_entity_obj)

    @staticmethod
    def handle_created(entity_type, entity_obj):
        Notifier.notify(ActionType.CREATED, entity_obj)

    @staticmethod
    def handle_deleted(entity_type, entity_obj):
        Notifier.notify(ActionType.DELETED, entity_obj)

    @staticmethod
    def handle_updated(entity_type, entity_obj, original_entity_obj):
        if original_entity_obj.is_deleted != entity_obj.is_deleted:
            Notifier.notify(ActionType.UPDATED.value.IS_DELETED, entity_obj)
        elif entity_type in Notifier.ENTITY_NOTIFICATION_MAP:
            notification_fn = Notifier.ENTITY_NOTIFICATION_MAP[entity_type]
            status = notification_fn(entity_obj, original_entity_obj)
            if status:
                Notifier.notify(status, entity_obj)

    @classmethod
    def notify(cls, action, entity_obj):
        print(f"Notifying for {entity_obj.notify_on}: {entity_obj.notify_on.pk}, trigger: {action}")



    ENTITY_NOTIFICATION_MAP = {
        "Company": notify_company,
        "Event": notify_event,
        "Webinar": notify_webinar,
        "ContentItem": notify_content_item,
        "CompanyForEvent": notify_company_for_event,
        "CompanyForWebinar": notify_company_for_webinar,
    }
