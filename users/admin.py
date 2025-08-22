from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from .models import UserProfile
from django.urls import reverse


class UserProfileInline(admin.StackedInline):
    """Inline admin for UserProfile"""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


class UserAdmin(BaseUserAdmin):
    """Custom User admin with profile inline"""
    inlines = (UserProfileInline,)
    list_display = ['username', 'email', 'first_name', 'last_name', 'role_display', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active', 'profile__role']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    def role_display(self, obj):
        """Display user role"""
        if hasattr(obj, 'profile'):
            return obj.profile.get_role_display()
        return 'No Role'
    role_display.short_description = 'Role'


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin interface for UserProfile model"""
    
    list_display = [
        'user_display', 'role_display', 'phone_number', 'department', 
        'employee_id', 'created_at'
    ]
    list_filter = ['role', 'created_at']
    search_fields = [
        'user__username', 'user__email', 'user__first_name', 'user__last_name',
        'phone_number', 'employee_id'
    ]
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'role')
        }),
        ('Personal Information', {
            'fields': ('phone_number', 'address', 'date_of_birth', 'profile_picture')
        }),
        ('Professional Information', {
            'fields': ('department', 'employee_id')
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user_display(self, obj):
        """Display user with link"""
        url = reverse('admin:auth_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.get_full_name() or obj.user.username)
    user_display.short_description = 'User'
    user_display.admin_order_field = 'user__username'
    
    def role_display(self, obj):
        """Display role with color coding"""
        colors = {
            'admin': '#dc3545',      # Red
            'staff': '#0066cc',      # Blue
            'teacher': '#28a745',    # Green
            'parent': '#ffc107',     # Yellow
            'student': '#6c757d',    # Gray
        }
        color = colors.get(obj.role, '#6c757d')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.get_role_display()
        )
    role_display.short_description = 'Role'
    role_display.admin_order_field = 'role'
