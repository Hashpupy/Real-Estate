from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions

class IsOwnerOrAgent(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or getattr(request.user, 'user_type', None) == 'agent'

class IsAgentOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(request.user, 'user_type', None) == 'agent'
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100