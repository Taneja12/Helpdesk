# from rest_framework import serializers
# from django.contrib.auth import get_user_model
# from .models import Ticket

# User = get_user_model()


# class TicketSerializer(serializers.ModelSerializer):
#     created_by = serializers.ReadOnlyField(source="created_by.username")
#     assigned_to = serializers.CharField(source="assigned_to.username", read_only=True)

#     class Meta:
#         model = Ticket
#         fields = [
#             "id",
#             "title",
#             "description",
#             "priority",
#             "status",
#             "created_by",
#             "assigned_to",
#             "created_at",
#             "updated_at",
#         ]
#         read_only_fields = ["status"]  # users cannot change status

#     def create(self, validated_data):
#         user = self.context["request"].user
#         validated_data["created_by"] = user
#         return super().create(validated_data)


# class AssignTicketSerializer(serializers.Serializer):
#     agent_username = serializers.CharField()

#     def validate_agent_username(self, value):
#         try:
#             user = User.objects.get(username=value)
#         except User.DoesNotExist:
#             raise serializers.ValidationError("Agent not found")

#         if user.role != "agent":
#             raise serializers.ValidationError("Selected user is not an agent")

#         return value


# class AgentStatusUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Ticket
#         fields = ["status"]

#     def validate_status(self, value):
#         if value not in [Ticket.STATUS_IN_PROGRESS, Ticket.STATUS_RESOLVED, Ticket.STATUS_CLOSED]:
#             raise serializers.ValidationError("Invalid status for agent update")
#         return value


from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Ticket

User = get_user_model()


class TicketSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source="created_by.username", read_only=True)
    assigned_to = serializers.CharField(source="assigned_to.username", read_only=True)

    class Meta:
        model = Ticket
        fields = [
            "id",
            "title",
            "description",
            "priority",
            "status",
            "created_by",
            "assigned_to",
            "created_at",
            "updated_at",
        ]


class AssignTicketSerializer(serializers.Serializer):
    agent_username = serializers.CharField()

    def validate_agent_username(self, value):
        try:
            user = User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Agent does not exist")

        if user.role != "agent":
            raise serializers.ValidationError("Selected user is not an agent")
        
        return value


class AgentStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["status"]

    def validate_status(self, value):
        if value not in [
            Ticket.STATUS_IN_PROGRESS,
            Ticket.STATUS_RESOLVED,
            Ticket.STATUS_CLOSED,
        ]:
            raise serializers.ValidationError("Invalid status for agent update")
        return value
