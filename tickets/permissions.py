from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "admin"


# class IsTicketOwner(BasePermission):
#     """User can access only tickets they created"""
#     def has_object_permission(self, request, view, obj):
#         return obj.created_by == request.user


# class IsAssignedAgent(BasePermission):
#     """Agent can access only tickets assigned to them"""
#     def has_object_permission(self, request, view, obj):
#         return obj.assigned_to == request.user


class TicketAccessPermission(BasePermission):
    """
    Admin → access all  
    Agent → only assigned  
    User → only own tickets  
    """

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True
        if request.user.role == "agent":
            return obj.assigned_to == request.user
        return obj.created_by == request.user

class CanCreateTicket(BasePermission):
    """
    Only normal users and admins can create tickets.
    Agents cannot create tickets.
    """

    def has_permission(self, request, view):
        # Only applies on POST
        if request.method == "POST" and request.user.role == "agent":
            return False
        return True
    
