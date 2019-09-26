import json
import asyncio
from requests.exceptions import HTTPError

# Django
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponse, Http404
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

# Django Rest Framework Files
from rest_framework import generics, permissions, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes

# Django Rest Framework JWT
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework_jwt.settings import api_settings

# Social Login
from social_django.utils import load_strategy, load_backend
from social_core.backends.oauth import BaseOAuth2
from social_core.exceptions import MissingBackend, AuthTokenError, AuthForbidden

# Local
from .models import (Users)
from .serializer import (UserSerializer, SocialSerializer, CheckUserSerializer)
from .token import signup
from comman import response

# Payload Custom Variables
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER

# Asyncio loop
loop = asyncio.get_event_loop()


# Check if user exists
@api_view(['POST'])
@permission_classes((AllowAny,))
def checkUser(request):
    if request.method == 'POST':
        serializer = CheckUserSerializer(data=request.data)
        if serializer.is_valid():
            # check if email exists
            email = request.data.get('email')
            user = Users.objects.filter(email=email).exists()
            if user is False:
                response_data = {
                    'key': 1
                }
                return response.MessageWithStatusSuccessAndData(True, 'Add password to complete registeration.', response_data, status.HTTP_200_OK)
            else:
                response_data = {
                    'key': 2
                }
                return response.MessageWithStatusSuccessAndData(True, 'Enter password to login.', response_data, status.HTTP_200_OK)
        else:
            return response.SerializerError(details=serializer.errors)
    else:
        return response.Error400WithMessage('Bad Request.')


# register
@api_view(['POST'])
@permission_classes((AllowAny,))
def registerUser(request):
    if request.method == 'POST':
        # add data to user table
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['active'] = True
            serializer.validated_data['verified'] = False
            serializer.validated_data['complete'] = False
            serializer.validated_data['user_type'] = 'IN'
            user = serializer.save()

            # sending verification email
            loop.run_in_executor(
                None, sendVerificationMail, user, serializer.validated_data['email'])

            return response.MessageWithStatusAndSuccess(True, 'User registered successfully.', status.HTTP_201_CREATED)
        else:
            return response.SerializerError(details=serializer.errors)

    else:
        return response.Error400WithMessage('Bad Request.')


# Send Verification Mail Function
def sendVerificationMail(user, to_email):
    mail_subject = 'Verify Your E-mail Address.'
    message = render_to_string('verify_email.html', {
        'user': user,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': signup.account_activation_token.make_token(user),
    })
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.content_subtype = "html"
    email.send()


# Verify email
@api_view(['POST', 'PUT'])
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
        user = Users.objects.filter(pk=uid).update(verified=True)

        return response.MessageWithStatusAndSuccess(True, 'Email verified successfully.', status.HTTP_202_ACCEPTED)
    else:
        return response.Error400WithMessage('Activation link is invalid.')


# Authenticate class
class Authenticate(ObtainJSONWebToken):
    def post(self, request, *args, **kwargs):
        res = super(Authenticate, self).post(request, *args, **kwargs)
        token = res.data.get('token')

        # token ok, get user
        if token:
            user = jwt_decode_handler(token)  # aleady json - don't serialize
        else:  # if none, try auth by email
            req = request.data  # try and find email in request
            password = req.get('password')
            email = req.get('email')
            if email is None or password is None:
                return response.Error400WithMessage('Missing or incorrect credentials.')

            try:
                user = Users.objects.get(email=email)
            except Users.DoesNotExist:
                return response.MessageWithStatusAndSuccess(False, 'User not found.', status.HTTP_404_NOT_FOUND)

            if not user.check_password(password):
                return response.MessageWithStatusAndSuccess(False, 'Incorrect password.', status.HTTP_403_FORBIDDEN)

            user = UserSerializer(user).data
            token = jwt_encode_handler(jwt_payload_handler(user))

        response_data = {
            'token': token
        }
        return response.MessageWithStatusSuccessAndData(True, 'User authenticated.', response_data, status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def userDetails(request):
    try:
        uid = str(request.user)
        user = Users.objects.get(pk=uid)
    except(Users.DoesNotExist):
        user = None

    if user is not None:
        serializer = UserSerializer(user).data
        response_data = {
            'user': serializer
        }
        return response.MessageWithStatusSuccessAndData(True, 'User data.', response_data, status.HTTP_200_OK)
    else:
        return response.Error400WithMessage('Invalid user.')


# Log in using social oAuth
class OAuthenticate(generics.GenericAPIView):
    serializer_class = SocialSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        # Authenticate user through the provider and access_token
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        provider = serializer.data.get('provider', None)
        strategy = load_strategy(request)

        try:
            backend = load_backend(
                strategy=strategy, name=provider, redirect_uri=None)

        except MissingBackend:
            return response.Error400WithMessage('Please provide a valid provider.')

        try:
            if isinstance(backend, BaseOAuth2):
                access_token = serializer.data.get('access_token')
            user = backend.do_auth(access_token)

        except HTTPError as error:
            return response.ErrorMessageWithStatusAndDetails('Invalid token.', status.HTTP_400_BAD_REQUEST, str(error))

        except AuthTokenError as error:
            return response.ErrorMessageWithStatusAndDetails('Invalid credentials.', status.HTTP_400_BAD_REQUEST, str(error))

        try:
            user = backend.do_auth(access_token, user=user)

        except HTTPError as error:
            return response.ErrorMessageWithStatusAndDetails('Invalid token.', status.HTTP_400_BAD_REQUEST, str(error))

        except AuthForbidden as error:
            return response.ErrorMessageWithStatusAndDetails('Invalid token.', status.HTTP_400_BAD_REQUEST, str(error))

        if user and user.is_active:
            # generate JWT token
            token = jwt_encode_handler(jwt_payload_handler(user))

            response_data = {
                'token': token
            }
            return response.MessageWithStatusSuccessAndData(True, 'User authenticated.', response_data, status.HTTP_200_OK)
