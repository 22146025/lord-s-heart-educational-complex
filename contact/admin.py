from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Admin interface for ContactMessage model"""
    
    list_display = [
        'name_display', 'email_display', 'status_display', 'created_at',
        'message_preview', 'ip_address'
    ]
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = [
        'created_at', 'updated_at', 'read_at', 'replied_at', 'ip_address', 'user_agent'
    ]
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'message')
        }),
        ('Status Information', {
            'fields': ('status', 'created_at', 'read_at', 'replied_at')
        }),
        ('Technical Information', {
            'fields': ('ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_replied', 'archive_messages']
    
    def name_display(self, obj):
        """Display name with link to detail view"""
        url = reverse('admin:contact_contactmessage_change', args=[obj.id])
        return format_html('<a href="{}">{}</a>', url, obj.name)
    name_display.short_description = 'Name'
    name_display.admin_order_field = 'name'
    
    def email_display(self, obj):
        """Display email as clickable mailto link"""
        return format_html('<a href="mailto:{}">{}</a>', obj.email, obj.email)
    email_display.short_description = 'Email'
    email_display.admin_order_field = 'email'
    
    def status_display(self, obj):
        """Display status with color coding"""
        colors = {
            'new': '#dc3545',      # Red
            'read': '#0066cc',     # Blue
            'replied': '#28a745',  # Green
            'archived': '#6c757d', # Gray
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.get_status_display()
        )
    status_display.short_description = 'Status'
    status_display.admin_order_field = 'status'
    
    def message_preview(self, obj):
        """Display a preview of the message"""
        preview = obj.message[:100] + '...' if len(obj.message) > 100 else obj.message
        return format_html('<span title="{}">{}</span>', obj.message, preview)
    message_preview.short_description = 'Message Preview'
    
    def mark_as_read(self, request, queryset):
        """Action to mark selected messages as read"""
        updated = 0
        for message in queryset:
            if message.status == 'new':
                message.mark_as_read()
                updated += 1
        
        self.message_user(
            request, 
            f'Successfully marked {updated} message(s) as read.'
        )
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_replied(self, request, queryset):
        """Action to mark selected messages as replied"""
        updated = 0
        for message in queryset:
            message.mark_as_replied()
            updated += 1
        
        self.message_user(
            request, 
            f'Successfully marked {updated} message(s) as replied.'
        )
    mark_as_replied.short_description = "Mark selected messages as replied"
    
    def archive_messages(self, request, queryset):
        """Action to archive selected messages"""
        updated = 0
        for message in queryset:
            message.archive()
            updated += 1
        
        self.message_user(
            request, 
            f'Successfully archived {updated} message(s).'
        )
    archive_messages.short_description = "Archive selected messages"
    
    def get_queryset(self, request):
        """Custom queryset with optimized ordering"""
        return super().get_queryset(request).order_by('-created_at')
    
    def has_add_permission(self, request):
        """Disable adding messages through admin (they come from contact form)"""
        return False
