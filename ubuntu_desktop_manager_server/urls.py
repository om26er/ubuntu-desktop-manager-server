from django.conf.urls import url, include
from django.contrib import admin

from ubuntu_desktop_manager_app import urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(urls)),
]
