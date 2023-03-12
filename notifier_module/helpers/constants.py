from enum import Enum


class UpdateTypes(Enum):
    IS_DELETED = "is_deleted_updated"
    CRAWLING_STATUS = "crawling_status_updated"
    IS_BLACKLISTED = "is_blacklisted_updated"


class ActionType(Enum):
    DELETED = "deleted"
    CREATED = "created"
    UPDATED = UpdateTypes
