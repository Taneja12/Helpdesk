from django.urls import path
from .views import (
    RegisterView, LoginView, LogoutView, ProfileView,
    UserSearchView, AdminCreateUserView
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("me/", ProfileView.as_view(), name="profile"),
    path("search/", UserSearchView.as_view(), name="user-search"),
    path("admin/create-user/", AdminCreateUserView.as_view(), name="admin-create-user"),
]
