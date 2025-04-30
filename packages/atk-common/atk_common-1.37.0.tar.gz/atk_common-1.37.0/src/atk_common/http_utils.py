from flask import Response
import json
from http import HTTPStatus
from atk_common.datetime_utils import get_utc_date_time
from atk_common.enums.api_error_type_enum import ApiErrorType
from atk_common.error_utils import get_error_entity, resend_error_entity
from atk_common.response_utils import is_response_http

def is_http_status_ok(status_code):
    return status_code >= HTTPStatus.OK.value and status_code < HTTPStatus.MULTIPLE_CHOICES.value

def is_http_status_internal(status_code):
    return status_code >= HTTPStatus.INTERNAL_SERVER_ERROR.value

def get_test_response(docker_container_data, component):
    data = {}
    data['utcDateTime'] = get_utc_date_time()
    if docker_container_data is None:
        data['containerData'] = None
        data['component'] = component
    else:
        data['containerData'] = docker_container_data
    return data

# If response['status'] == 0 (OK, http status = 200): create Response and return response['responseMsg']   
# If http status == 500: 
#   If response['status'] == 1 (HTTP): resend received error entity
#   If response['status'] == 2 (INTERNAL): create new error entity and return as response
# If http status other value: create new error entity and return as response
def create_http_response(method, response, container_info):
    if is_http_status_ok(response['statusCode']):
        return Response(
            response=json.dumps(response['responseMsg']),
            status=HTTPStatus.OK,
            mimetype='application/json'
        )
    if is_http_status_internal(response['statusCode']):
        if is_response_http(response):
            resend_error_entity(response['responseMsg'])
        return get_error_entity(response['responseMsg'], method, ApiErrorType.INTERNAL, response['statusCode'], container_info)
    return get_error_entity(response['responseMsg'], method, ApiErrorType.CONNECTION, response['statusCode'], container_info)

