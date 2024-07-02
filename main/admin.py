from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Customers, Doctors, Category, Service, Orders, CashBoxLog
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'full_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'groups')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('full_name', 'age', 'address', 'phone_number')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'full_name', 'age', 'address', 'phone_number', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'full_name')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)
admin.site.register(User, CustomUserAdmin)

# Register other models
admin.site.register(Customers)
admin.site.register(Doctors)
admin.site.register(Category)
admin.site.register(Service)
admin.site.register(Orders)
admin.site.register(CashBoxLog)
