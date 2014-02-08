__author__ = 'srd1g10'
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class PassengerPermissions(permissions.BasePermission):
    """
    Permissions class to handle Passenger.
    Passenger can update their own position but not read it.
    """
    def has_permission(self, request, view):
        return request.method == 'PATCH'

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class DriverCheckInPermissions(permissions.BasePermission):
    """
    Permissions class to handle Driver check in.
    Driver can read the list of requests near them.
    """
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class DriverUpdatePositionPermissions(permissions.BasePermission):
    """
    Permissions class to handle Driver updating position.
    Driver can write their position but not read.
    """
    def has_object_permission(self, request, view, obj):
        return (obj.owner == request.user) and (request.method == 'PATCH')