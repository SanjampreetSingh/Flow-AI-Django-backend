from datetime import datetime
from calendar import timegm
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import user_logged_in


def jwt_payload_handler(user):
    """ Custom payload handler
    Token encrypts the dictionary returned by this function, and can be decoded by rest_framework_jwt.utils.jwt_decode_handler
    """
    user_logged_in.send(sender=user.__class__, user=user)
    return {
        'user_id': user.id,
        'username': user.email,
        'email': user.email,
        'user_type': user.user_type,
        'is_complete': user.complete,
        'steps': user.steps,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA,
        'orig_iat': timegm(
            datetime.utcnow().utctimetuple()
        )
    }


def jwt_response_payload_handler(token, user=None, request=None):
    """ Custom response payload handler.

    This function controlls the custom payload after login or token refresh. This data is returned through the web API.
    """
    return {
        'token': token,
        'user_id': user.id,
        'username': user.email,
        'email': user.email,
        'user_type': user.user_type,
        'is_complete': user.complete,
        'steps': user.steps,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA,
        'orig_iat': timegm(
            datetime.utcnow().utctimetuple()
        )
    }
