from django.contrib import admin

from ubuntu_desktop_manager_app.models import User


class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = User

admin.site.register(User, UserAdmin)
