from api.models import CRAWLING_STATUSES
from notifier_module.helpers.constants import ActionType


def get_crawling_status(entity_obj, original_entity_obj):
    if entity_obj.crawling_status in [CRAWLING_STATUSES[0], CRAWLING_STATUSES[1]] \
            and not entity_obj.crawling_status != original_entity_obj.crawling_status and original_entity_obj:
        return ActionType.UPDATED.value.CRAWLING_STATUS
    return None


def get_is_blacklisted(entity_obj, original_entity_obj):
    if entity_obj.is_blacklisted != original_entity_obj.is_blacklisted and original_entity_obj:
        return ActionType.UPDATED.value.IS_BLACKLISTED
    return None


def notify_company(entity_obj, original_entity_obj):
    return get_crawling_status(entity_obj, original_entity_obj)


def notify_event(entity_obj, original_entity_obj):
    return get_crawling_status(entity_obj, original_entity_obj) or get_is_blacklisted(entity_obj, original_entity_obj)


def notify_webinar(entity_obj, original_entity_obj):
    return get_crawling_status(entity_obj, original_entity_obj) or get_is_blacklisted(entity_obj,
                                                                                              original_entity_obj)


def notify_content_item(entity_obj, original_entity_obj):
    return get_crawling_status(entity_obj, original_entity_obj) or get_is_blacklisted(entity_obj,
                                                                                              original_entity_obj)


def notify_company_for_event(entity_obj, original_entity_obj):
    return get_is_blacklisted(entity_obj, original_entity_obj)


def notify_company_for_webinar(entity_obj, original_entity_obj):
    return get_is_blacklisted(entity_obj, original_entity_obj)