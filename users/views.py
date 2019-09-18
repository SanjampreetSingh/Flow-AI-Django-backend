import json
from requests.exceptions import HTTPError

# Django
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.http import HttpResponse, Http404, JsonResponse
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
from .serializer import (UserSerializer, SocialSerializer)
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
                serializer.validated_data['active'] = True
                serializer.validated_data['verified'] = False
                serializer.validated_data['complete'] = False
                serializer.validated_data['user_type'] = 'IN'
                user = serializer.save()

                # email sending code
                current_site = get_current_site(request)
                mail_subject = 'Verify Your E-mail Address.'
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

                return Response(
                    {
                        'success': True,
                        'message': 'User Registered Successfully',
                    },
                    status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {
                        'success': False,
                        'message': str(serializer.errors)
                    },
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {
                    'success': False,
                    'message': 'User already exists'
                },
                status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(
            {
                'success': False,
                'message': 'Bad Request'
            },
            status=status.HTTP_400_BAD_REQUEST)


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

        return Response(
            {
                'success': True,
                'message': 'Email verified successfully.'
            },
            status=status.HTTP_202_ACCEPTED)
    else:
        return Response(
            {
                'success': False,
                'message': 'Activation link is invalid.'
            },
            status=status.HTTP_400_BAD_REQUEST)


# Login class
class LoginAPI(ObtainJSONWebToken):
    def post(self, request, *args, **kwargs):
        response = super(LoginAPI, self).post(request, *args, **kwargs)
        token = response.data.get('token')

        # token ok, get user
        if token:
            user = jwt_decode_handler(token)  # aleady json - don't serialize
        else:  # if none, try auth by email
            req = request.data  # try and find email in request
            password = req.get('password')
            email = req.get('email')
            if email is None or password is None:
                return Response(
                    {
                        'success': False,
                        'message': 'Missing or incorrect credentials',
                    },
                    status=status.HTTP_400_BAD_REQUEST)

            try:
                user = Users.objects.get(email=email)
            except Users.DoesNotExist:
                return Response(
                    {
                        'success': False,
                        'message': 'User not found',
                    },
                    status=status.HTTP_404_NOT_FOUND)

            if not user.check_password(password):
                return Response(
                    {
                        'success': False,
                        'message': 'Incorrect password',
                    },
                    status=status.HTTP_403_FORBIDDEN)

            user = UserSerializer(user).data
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

        return Response(
            {
                'success': True,
                'message': 'User authenticated'
            },
            status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def get_user(request):
    try:
        uid = str(request.user)
        user = Users.objects.get(pk=uid)
    except(Users.DoesNotExist):
        user = None

    if user is not None:
        serializer = UserSerializer(user).data
        return Response(
            {
                'success': True,
                'user': serializer
            },
            status=status.HTTP_200_OK)
    else:
        return Response(
            {
                'success': False,
                'message': 'Invalid user'
            },
            status=status.HTTP_400_BAD_REQUEST)


class SocialLoginView(generics.GenericAPIView):
    # Log in using social oAuth
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
            return Response(
                {
                    'success': False,
                    'message': 'Please provide a valid provider'
                },
                status=status.HTTP_400_BAD_REQUEST)
        try:
            if isinstance(backend, BaseOAuth2):
                access_token = serializer.data.get('access_token')
            user = backend.do_auth(access_token)

        except HTTPError as error:
            return Response(
                {
                    'success': False,
                    'message': 'Invalid token',
                    'details': str(error)
                },
                status=status.HTTP_400_BAD_REQUEST)

        except AuthTokenError as error:
            return Response(
                {
                    'success': False,
                    'message': 'Invalid credentials',
                    'details': str(error)
                },
                status=status.HTTP_400_BAD_REQUEST)

        try:
            user = backend.do_auth(access_token, user=user)

        except HTTPError as error:
            return Response(
                {
                    'success': False,
                    'message': 'Invalid token',
                    'details': str(error)
                },
                status=status.HTTP_400_BAD_REQUEST)

        except AuthForbidden as error:
            return Response(
                {
                    'success': False,
                    'message': 'Invalid token',
                    'details': str(error)
                },
                status=status.HTTP_400_BAD_REQUEST)

        if user and user.is_active:
            # generate JWT token
            data = {
                'token': jwt_encode_handler(
                    jwt_payload_handler(user)
                )}
            return Response(
                {
                    'success': True,
                    'message': 'User authenticated'
                },
                status=status.HTTP_200_OK)
