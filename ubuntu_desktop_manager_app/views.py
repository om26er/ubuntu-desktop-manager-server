from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated, BasePermission

from simple_login.views import (
    RetrieveUpdateDestroyProfileAPIView,
    LoginAPIView,
    PasswordResetRequestAPIView,
    PasswordChangeAPIView,
    StatusAPIView,
)

from ubuntu_desktop_manager_app.models import Device, User
from ubuntu_desktop_manager_app.serializers import (
    DeviceSerializer,
    UserSerializer,
)


class Register(CreateAPIView):
    serializer_class = UserSerializer


class Login(LoginAPIView):
    user_model = User
    serializer_class = UserSerializer


class Profile(RetrieveUpdateDestroyProfileAPIView):
    user_model = User
    serializer_class = UserSerializer


class ForgotPassword(PasswordResetRequestAPIView):
    user_model = User
    serializer_class = UserSerializer


class ChangePassword(PasswordChangeAPIView):
    user_model = User
    serializer_class = UserSerializer


class Status(StatusAPIView):
    user_model = User
    serializer_class = UserSerializer


class DeviceRegisterAPIView(CreateAPIView):
    serializer_class = DeviceSerializer
    permission_classes = (IsAuthenticated, )


class DeviceListAPIView(ListAPIView):
    serializer_class = DeviceSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Device.objects.filter(user=self.request.user)


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class DeviceAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = DeviceSerializer
    permission_classes = (IsAuthenticated, IsOwner, )

    def get_object(self):
        return Device.object.get(id=int(self.kwargs['pk']))
