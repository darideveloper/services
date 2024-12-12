from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status'] = "error"
        details = response.data.get('detail', None)
        del response.data['detail']
        if details:
            response.data['message'] = details
        else:
            response.data['message'] = "Invalid data"
        response.data['data'] = {}

    return response