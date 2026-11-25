"""
healthcare_project/exceptions.py — Standardized DRF Exception Handler

Converts all API exceptions (validation errors, 401s, 403s, 404s, 500s)
into a consistent, predictable JSON schema across the entire application:

{
    "success": false,
    "status_code": 400,
    "message": "A human-readable summary of the error",
    "errors": {
        "field_name": ["Specific error detail"]
    }
}
"""

from rest_framework.views import exception_handler
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler that intercepts DRF exceptions and returns
    a standardized JSON response format.
    """
    # Call REST framework's default exception handler first to get the standard response
    response = exception_handler(exc, context)

    if response is not None:
        custom_data = {
            'success': False,
            'status_code': response.status_code,
        }

        # Determine error message and formatted errors dict
        if isinstance(response.data, dict):
            # If detail is present (e.g. 401, 403, 404)
            if 'detail' in response.data:
                custom_data['message'] = str(response.data['detail'])
                custom_data['errors'] = {'detail': response.data['detail']}
            else:
                # Validation error dictionary
                custom_data['message'] = 'Validation failed.'
                custom_data['errors'] = response.data
        elif isinstance(response.data, list):
            custom_data['message'] = 'Validation failed.'
            custom_data['errors'] = {'non_field_errors': response.data}
        else:
            custom_data['message'] = 'An unexpected error occurred.'
            custom_data['errors'] = {'detail': str(response.data)}

        response.data = custom_data

    return response
