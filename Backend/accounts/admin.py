from django.contrib import admin
from .models import CustomUser,Role

# Register your models here.


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display=["name"]

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', "display_roles", 'phone')
    search_fields = ('username', 'email', 'role', 'phone')



    def display_roles(self, obj):
        return ", ".join([role.name for role in obj.role.all()])

    display_roles.short_description = "Role" 
