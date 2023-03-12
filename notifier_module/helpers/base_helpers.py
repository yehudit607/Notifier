import logging
import traceback
from http import HTTPStatus
from django.http import JsonResponse


def general_exception():
    logger.error("notifier service  general Exception, exception is:")
    traceback.print_exc()
    return JsonResponse(
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
        data={"error": "notifier service  general Exception"}
    )


def get_session_logger():
    return logging.getLogger("notifier")


logger = get_session_logger()
