from rest_framework import filters, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from drf_spectacular.utils import extend_schema, OpenApiTypes
from django.contrib.auth import get_user_model

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    AdminCreateUserSerializer,
)
from .permissions import IsAdmin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


User = get_user_model()

# REGISTER
@extend_schema(
    request=RegisterSerializer,
    responses=UserSerializer,
)
 
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


# LOGIN
 
class LoginView(APIView):
    @extend_schema(
        request=LoginSerializer,
        responses={200: UserSerializer},
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        login(request, user)
        # Return the serialized user data
        return Response({"message": "Login successful", "user": UserSerializer(user).data}, status=status.HTTP_200_OK)


# # LOGOUT
# @extend_schema(
#     request=None,
#     responses={200: OpenApiTypes.OBJECT},
# )
 
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logged out"}, status=status.HTTP_200_OK)


# PROFILE
 
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=UserSerializer,
    )
    def get(self, request):
        return Response(UserSerializer(request.user).data)

    @extend_schema(
        request=UserSerializer,
        responses=UserSerializer,
    )
    def put(self, request):
        # Ensure role cannot be updated via profile
        data = request.data.copy()
        data.pop('role', None)
        serializer = UserSerializer(request.user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        responses={200: None},
    )
    def delete(self, request):
        request.user.delete()
        return Response({"message": "Account deleted"}, status=status.HTTP_200_OK)


# USER SEARCH
@extend_schema(
    responses=UserSerializer(many=True),
)
 
class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']

    def get_queryset(self):
        # Admins can search all users
        if self.request.user.role == 'admin':
            return User.objects.all()
        # Non-admins can only search themselves (or you could restrict entirely)
        return User.objects.filter(id=self.request.user.id)


# ADMIN: Create user with role (admin-only endpoint)
@extend_schema(
    request=AdminCreateUserSerializer,
    responses=UserSerializer,
)
class AdminCreateUserView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = AdminCreateUserSerializer
