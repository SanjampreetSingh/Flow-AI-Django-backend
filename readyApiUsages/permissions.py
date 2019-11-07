from rest_framework import permissions
from .models import (ReadyApiUsageBuckets)


class IsReadyApiUsageBucketsAppOwner(permissions.BasePermission):
    message = 'User must be owner of the application.'

    def has_permission(self, request, view):
        pk = int(view.kwargs['pk'])
        try:
            readyApiUsageBucket = ReadyApiUsageBuckets.objects.get(id=pk)
            user = readyApiUsageBucket.user.id
        except ReadyApiUsageBuckets.DoesNotExist:
            return False

        if request.user.id == user:
            return True
