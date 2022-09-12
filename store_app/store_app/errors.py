from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_409_CONFLICT


class SyncError(APIException):
    status = HTTP_409_CONFLICT
    default_detail = 'Synchronization failed'
    default_code = 'sync_failed'
