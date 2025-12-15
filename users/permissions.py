from rest_framework.permissions import BasePermission

class IsUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'user'

class IsAgent(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'agent'

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'admin'


# # Useful object-level permissions examples (for use with ticket objects)
# class IsOwnerOrAdmin(BasePermission):
#     """
#     Allow access if the user is the owner/creator of the object or an admin.
#     Expects the object to have `created_by` attribute.
#     """
#     def has_object_permission(self, request, view, obj):
#         if request.user.role == 'admin':
#             return True
#         return getattr(obj, 'created_by', None) == request.user

# class IsAssignedAgentOrAdmin(BasePermission):
#     """
#     Allow access if user is the assigned agent or admin.
#     Expects the object to have `assigned_to` attribute.
#     """
#     def has_object_permission(self, request, view, obj):
#         if request.user.role == 'admin':
#             return True
#         return getattr(obj, 'assigned_to', None) == request.user
