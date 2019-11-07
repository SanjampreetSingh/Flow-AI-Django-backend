import asyncio

# django
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string

# Django Rest Framework Files
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes

# Django Rest Framework JWT
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# Local
from apps.models import (
    Apps
)
from users.models import (
    Users
)
from .models import (
    ReadyApiUsageBuckets
)
from .serializer import (
    ReadyApiUsageBucketsWriteSerializer,
    ReadyApiUsageBucketsReadSerializer
)

# from comman.boto import()
from comman.permissions import (HasVerifiedEmail)
from comman import response

# Asyncio loop
loop = asyncio.get_event_loop()


class ReadyApiUsageBucketsView(viewsets.ModelViewSet):
    queryset = ReadyApiUsageBuckets.objects.all()
    permission_classes = [IsAuthenticated, HasVerifiedEmail]
    authentication_classes = [JSONWebTokenAuthentication]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReadyApiUsageBucketsWriteSerializer
        return ReadyApiUsageBucketsReadSerializer

    def list(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def create(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, pk=None):
        # to be coded
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


def increase_ready_call(api_key):
    app = (Apps.objects.filter(apikey_value=api_key))[0]
    ready_usage_bucket = (
        ReadyApiUsageBuckets.objects.get_or_create(app=app))[0]

    if ready_usage_bucket.usage < ready_usage_bucket.bucket:
        ready_usage_bucket.usage += 1
        ready_usage_bucket.save()

        if ready_usage_bucket.usage == ready_usage_bucket.threshold:
            user = (Users.objects.filter(pk=app.user))[0]
            loop.run_in_executor(None, sendThresholdMail, user, user.email)

        if ready_usage_bucket.usage == ready_usage_bucket.bucket:
            # boto update enable
            app.active = False
            app.save()
        return response.MessageWithStatusAndSuccess(True, 'Call made successfully.', status.HTTP_200_OK)

    elif ready_usage_bucket.usage == ready_usage_bucket.bucket:
        # boto update enable
        app.active = False
        app.save()
        return response.Error400WithMessage('Usage qouta is full, to make more calls increase usage quota.')

    else:
        return response.Error400WithMessage('Usage qouta is full, to make more calls increase usage quota.')


# Send Verification Mail Function
def sendThresholdMail(user, to_email):
    mail_subject = 'App Usage Bucket about to get full!'
    message = render_to_string('ready_threshold_email.html', {
        'user': user,
    })
    email = EmailMessage(
        mail_subject, message, 'Flow <no-reply@theflowai.com> ', to=[to_email]
    )
    email.content_subtype = "html"
    email.send()
