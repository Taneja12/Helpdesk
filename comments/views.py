from rest_framework import viewsets, permissions
from django.db import models
from .models import Comment
from .serializers import CommentSerializer
from tickets.models import Ticket

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        ticket_id = self.kwargs['ticket_id']
        user = self.request.user
        
        # Filter comments based on user's access to the ticket
        if user.role == 'admin':
            return Comment.objects.filter(ticket_id=ticket_id).order_by('-created_at')
        
        return Comment.objects.filter(
            ticket_id=ticket_id
        ).filter(
            models.Q(ticket__created_by=user) | models.Q(ticket__assigned_to=user)
        ).order_by('-created_at')

    def perform_create(self, serializer):
        ticket_id = self.kwargs['ticket_id']
        ticket = Ticket.objects.get(pk=ticket_id)
        user = self.request.user

        # Explicit permission check
        if user.role != 'admin' and ticket.created_by != user and ticket.assigned_to != user:
            raise permissions.PermissionDenied("You do not have access to this ticket.")

        serializer.save(ticket_id=ticket_id, user=user)
        
        # Update ticket timestamp explicitly to prevent premature escalation
        ticket.save()
