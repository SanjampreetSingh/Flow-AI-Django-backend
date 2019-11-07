from rest_framework import permissions


class HasCompleteProfile(permissions.BasePermission):
    message = 'Complete your profile first.'

    def has_permission(self, request, view):
        if request.user.complete is True:
            return True


class HasVerifiedEmail(permissions.BasePermission):
    message = 'Verify your email first.'

    def has_permission(self, request, view):
        if request.user.verified is True:
            return True


class IsApplicationOwner(permissions.BasePermission):
    message = 'User must be owner of the application.'

    def has_permission(self, request, view):
        user_id = int(view.kwargs['user_id'])
        if request.user.id == user_id:
            return True
