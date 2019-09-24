from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST


def SerializerError(details=None):
    return Response(
        {
            'success': False,
            'message': 'Invalid data.',
            'error':
            {
                'details': details
            }
        },
        status=HTTP_400_BAD_REQUEST)


def Error400WithMessage(message=None):
    return Response(
        {
            'success': False,
            'message': message
        },
        status=HTTP_400_BAD_REQUEST)


def ErrorMessageWithStatusAndDetails(message=None, status=None, details=None):
    return Response(
        {
            'success': False,
            'message': message,
            'error':
            {
                'details': details
            }
        },
        status=status)


def MessageWithStatusAndSuccess(success=True, message=None, status=None):
    return Response(
        {
            'success': success,
            'message': message
        },
        status=status)
