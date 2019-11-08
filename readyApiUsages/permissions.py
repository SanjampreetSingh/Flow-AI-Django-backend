from rest_framework import permissions
from .models import (ReadyApiUsageBuckets)


class IsReadyApiUsageBucketsAppOwner(permissions.BasePermission):
    message = 'User must be owner of the application.'

    def has_permission(self, request, view):
        app = int(view.kwargs['app'])
        try:
            readyApiUsageBucket = ReadyApiUsageBuckets.objects.filter(app=app)[
                0]
        except IndexError:
            return False
        try:
            user = readyApiUsageBucket.user.id
        except ReadyApiUsageBuckets.DoesNotExist:
            return False

        if request.user.id == user:
            return True
