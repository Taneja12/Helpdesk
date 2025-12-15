from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .models import Ticket
from .serializers import (
    TicketSerializer,
    AssignTicketSerializer,
    AgentStatusUpdateSerializer,
)
from .permissions import TicketAccessPermission, IsAdminRole, CanCreateTicket
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


User = get_user_model()


# USER: Create & list their own tickets
 
class TicketListCreateView(generics.ListCreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, CanCreateTicket]

    def get_queryset(self):
        qs = Ticket.objects.all()
        user = self.request.user

        # Role-based filtering
        if user.role == "agent":
            qs = qs.filter(assigned_to=user)
        elif user.role != "admin":
            qs = qs.filter(created_by=user)

        # Search filters
        title = self.request.query_params.get("title")
        status = self.request.query_params.get("status")
        priority = self.request.query_params.get("priority")
        assigned_to = self.request.query_params.get("assigned_to")

        if title:
            qs = qs.filter(title__icontains=title)
        if status:
            qs = qs.filter(status=status)
        if priority:
            qs = qs.filter(priority=priority)
        if assigned_to:
            qs = qs.filter(assigned_to__username=assigned_to)
        
        return qs

    

 
class TicketDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    permission_classes = [IsAuthenticated, TicketAccessPermission]

    def perform_destroy(self, instance):
        # Only admins can delete tickets
        if self.request.user.role != "admin":
            raise PermissionError("Only admins can delete tickets.")
        instance.delete()

class AssignTicketView(generics.GenericAPIView):
    serializer_class = AssignTicketSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

    def post(self, request, pk):
        ticket = Ticket.objects.get(pk=pk)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        agent_username = serializer.validated_data["agent_username"]
        agent = User.objects.get(username=agent_username)

        ticket.assigned_to = agent
        ticket.status = Ticket.STATUS_IN_PROGRESS
        ticket.save()

        return Response({
            "message": "Ticket assigned successfully",
            "assigned_to": agent.username
        })

class AgentUpdateStatusView(generics.GenericAPIView):
    serializer_class = AgentStatusUpdateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        ticket = Ticket.objects.get(pk=pk)
        self.check_object_permissions(request, ticket)

        # Strictly allow only "status"
        if "status" not in request.data:
            return Response({"error": "Status field is required"}, status=400)

        data = {"status": request.data["status"]}

        serializer = self.get_serializer(ticket, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"message": "Status updated"})


class TicketStatsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get(self, request):
        from django.utils import timezone
        from datetime import timedelta

        now = timezone.now()
        seven_days_ago = now - timedelta(days=7)

        # Count tickets created in last 7 days
        opened = Ticket.objects.filter(created_at__gte=seven_days_ago).count()

        # Count tickets resolved in last 7 days (using updated_at as proxy)
        resolved = Ticket.objects.filter(
            status=Ticket.STATUS_RESOLVED, 
            updated_at__gte=seven_days_ago
        ).count()

        # Count tickets escalated in last 7 days
        escalated = Ticket.objects.filter(
            status=Ticket.STATUS_ESCALATED, 
            updated_at__gte=seven_days_ago
        ).count()

        return Response({
            "period": "Last 7 Days",
            "opened": opened,
            "resolved": resolved,
            "escalated": escalated
        })
