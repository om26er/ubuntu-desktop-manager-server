from django.conf.urls import url

from ubuntu_desktop_manager_app.views import (
    ForgotPassword,
    ChangePassword,
    Register,
    Login,
    Profile,
    Status,
    DeviceRegisterAPIView,
    DeviceAPIView,
    DeviceListAPIView,
)


urlpatterns = [
    url(r'^api/user/register$', Register.as_view()),
    url(r'^api/user/login$', Login.as_view()),
    url(r'^api/user/forgot-password$', ForgotPassword.as_view()),
    url(r'^api/user/change-password$', ChangePassword.as_view()),
    url(r'^api/user/status$', Status.as_view()),
    url(r'^api/user/me$', Profile.as_view()),
    url(r'^api/user/device/register$', DeviceRegisterAPIView.as_view()),
    url(r'^api/user/device/', DeviceAPIView.as_view()),
    url(r'^api/user/devices$', DeviceListAPIView.as_view()),
]
