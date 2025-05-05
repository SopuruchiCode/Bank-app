from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser




class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["bvn","first_name","last_name","is_staff"]
    list_filter = ('is_staff','is_superuser','is_active')
    ordering = ("bvn",)

    fieldsets = (
        (None, {'fields': ('password',)}),
        ('Personal info',{'fields':('first_name','last_name')}),
        ('Permissions' , {'fields': ('is_active','is_staff','is_superuser', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name','last_name','password1','password2')
        }),
    )

    def get_fieldsets(self, request, obj= None):
        fieldsets = super().get_fieldsets(request, obj)
        # print("fieldsets:", fieldsets)
        return fieldsets

admin.site.register(CustomUser, CustomUserAdmin)


