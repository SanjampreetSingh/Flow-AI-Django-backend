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
