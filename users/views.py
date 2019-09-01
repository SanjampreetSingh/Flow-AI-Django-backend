# Django
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.http import HttpResponse, Http404
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

# Django Rest Framework Files
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes

# Django Rest Framework JWT
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework_jwt.settings import api_settings

# Local
from .models import (Users)
from .serializer import (UserSerializer)
from .token import signup

# Payload Custom Variables
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


# register
@api_view(['POST'])
@permission_classes((AllowAny,))
def register(request):
    if request.method == 'POST':

        # check if email exists
        email = request.data.get('email')
        user = Users.objects.filter(email=email).exists()
        if user is False:

            # add data to user table
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.validated_data['active'] = False
                serializer.validated_data['verified'] = False
                serializer.validated_data['complete'] = False
                serializer.validated_data['user_type'] = 'IN'
                serializer.validated_data['steps'] = 'NS'
                user = serializer.save()

                # email sending code
                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string('verify_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': signup.account_activation_token.make_token(user),
                })
                to_email = serializer.validated_data['email']
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()

                return Response({'success': True,
                                 'message': 'Please confirm your email address to complete the registration',
                                 'data': serializer.data},
                                status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('User already exists', status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response('Bad Request', status=status.HTTP_400_BAD_REQUEST)


# Verify email
@api_view(['POST', "PUT"])
@permission_classes((AllowAny,))
def verifyEmail(request, uidb64, token):
    # Check user exists by decoding url code
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Users.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Users.DoesNotExist):
        user = None

    # verify user and update verified, active status
    if user is not None and signup.account_activation_token.check_token(user, token):
        user = Users.objects.filter(pk=uid).update(verified=True, active=True)

        return Response({'user': user,
                         'message': 'Thank you for your email confirmation. Now you can login your account.'
                         },
                        status=status.HTTP_202_ACCEPTED)
    else:
        return Response({'message': 'Activation link is invalid!'},
                        status=status.HTTP_400_BAD_REQUEST)


# Login class
class LoginAPI(ObtainJSONWebToken):
    def post(self, request, *args, **kwargs):
        response = super(LoginAPI, self).post(request, *args, **kwargs)
        res = response.data
        token = res.get('token')

        # token ok, get user
        if token:
            user = jwt_decode_handler(token)  # aleady json - don't serialize
        else:  # if none, try auth by email
            req = request.data  # try and find email in request
            password = req.get('password')
            email = req.get('email')
            if email is None or password is None:
                return Response({'success': False,
                                 'message': 'Missing or incorrect credentials',
                                 'data': req},
                                status=status.HTTP_400_BAD_REQUEST)
            try:
                user = User.objects.get(email=email)
            except:
                return Response({'success': False,
                                 'message': 'User not found',
                                 'data': req},
                                status=status.HTTP_404_NOT_FOUND)

            if not user.check_password(password):
                return Response({'success': False,
                                 'message': 'Incorrect password',
                                 'data': req},
                                status=status.HTTP_403_FORBIDDEN)

            user = UserSerializer(user).data
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

        return Response({'success': True,
                         'message': 'Successfully logged in',
                         'token': token,
                         'user': user},
                        status=status.HTTP_200_OK)
