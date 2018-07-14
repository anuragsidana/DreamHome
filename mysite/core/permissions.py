from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):

        return request.user.profile.is_admin==True




