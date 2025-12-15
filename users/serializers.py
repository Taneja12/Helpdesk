from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from drf_spectacular.utils import extend_schema_field

User = get_user_model()


# ============================
# REGISTER SERIALIZER
# ============================
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=User.ROLE_USER,    # default user role
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# ============================
# LOGIN SERIALIZER
# ============================
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


# ============================
# USER SERIALIZER (with nameEmail)
# ============================
class UserSerializer(serializers.ModelSerializer):
    nameEmail = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'role',
            'first_name',
            'last_name',
            'nameEmail',
        ]
        read_only_fields = ['role', 'username']

    @extend_schema_field(serializers.CharField())
    def get_nameEmail(self, obj):
        """
        Assignment requirement:
        nameEmail = "FirstName LastName - Email"
        """
        full_name = f"{obj.first_name} {obj.last_name}".strip()
        return f"{full_name} - {obj.email}"


# ============================
# ADMIN CREATE USER SERIALIZER
# ============================
class AdminCreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'first_name', 'last_name']

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', User.ROLE_USER),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
