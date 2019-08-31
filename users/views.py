# django
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

# Django Rest Framework Files
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes

# Local
from .models import (Users)
from .serializer import (UserSerializer)
from .token import signup


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
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
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
