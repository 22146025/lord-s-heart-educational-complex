from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import AdmissionApplication


@admin.register(AdmissionApplication)
class AdmissionApplicationAdmin(admin.ModelAdmin):
    """Admin interface for AdmissionApplication model"""
    
    list_display = [
        'full_name_display', 'age', 'gender', 'class_before_admission', 
        'status_display', 'application_date', 'contact_info'
    ]
    list_filter = [
        'status', 'gender', 'class_before_admission', 'application_date',
        'region_of_birth', 'region_of_home_town'
    ]
    search_fields = [
        'surname', 'first_name', 'other_names', 'father_name', 'mother_name',
        'father_contact', 'mother_contact'
    ]
    readonly_fields = [
        'application_date', 'created_at', 'updated_at', 'full_name'
    ]
    fieldsets = (
        ('Pupil Information', {
            'fields': (
                'surname', 'first_name', 'other_names', 'date_of_birth', 'age',
                'gender', 'place_of_birth', 'region_of_birth', 'home_town',
                'region_of_home_town'
            )
        }),
        ('Previous Education', {
            'fields': (
                'last_school_attended', 'location_of_last_school',
                'class_before_admission', 'religious_denomination'
            )
        }),
        ('Personal Details', {
            'fields': ('hobbies', 'disability_or_allergy')
        }),
        ('Parent/Guardian Information', {
            'fields': (
                'father_name', 'mother_name', 'father_occupation', 'mother_occupation',
                'father_contact', 'mother_contact', 'father_email', 'mother_email'
            )
        }),
        ('Address Information', {
            'fields': ('postal_address', 'place_of_residence', 'house_number')
        }),
        ('Application Status', {
            'fields': (
                'status', 'application_date', 'reviewed_date', 'reviewed_by', 'notes'
            )
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_applications', 'reject_applications', 'mark_as_reviewed']
    
    def full_name_display(self, obj):
        """Display full name with link to detail view"""
        url = reverse('admin:admissions_admissionapplication_change', args=[obj.id])
        return format_html('<a href="{}">{}</a>', url, obj.full_name)
    full_name_display.short_description = 'Full Name'
    full_name_display.admin_order_field = 'surname'
    
    def status_display(self, obj):
        """Display status with color coding"""
        colors = {
            'pending': '#ffa500',  # Orange
            'reviewed': '#0066cc',  # Blue
            'accepted': '#28a745',  # Green
            'rejected': '#dc3545',  # Red
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.get_status_display()
        )
    status_display.short_description = 'Status'
    status_display.admin_order_field = 'status'
    
    def contact_info(self, obj):
        """Display contact information"""
        contacts = []
        if obj.father_contact:
            contacts.append(f"Father: {obj.father_contact}")
        if obj.mother_contact:
            contacts.append(f"Mother: {obj.mother_contact}")
        return mark_safe('<br>'.join(contacts)) if contacts else 'No contact'
    contact_info.short_description = 'Contact Info'
    
    def approve_applications(self, request, queryset):
        """Action to approve selected applications"""
        updated = queryset.update(status='accepted')
        self.message_user(
            request, 
            f'Successfully approved {updated} application(s).'
        )
    approve_applications.short_description = "Approve selected applications"
    
    def reject_applications(self, request, queryset):
        """Action to reject selected applications"""
        updated = queryset.update(status='rejected')
        self.message_user(
            request, 
            f'Successfully rejected {updated} application(s).'
        )
    reject_applications.short_description = "Reject selected applications"
    
    def mark_as_reviewed(self, request, queryset):
        """Action to mark applications as reviewed"""
        updated = queryset.update(status='reviewed')
        self.message_user(
            request, 
            f'Successfully marked {updated} application(s) as reviewed.'
        )
    mark_as_reviewed.short_description = "Mark selected applications as reviewed"
    
    def get_queryset(self, request):
        """Custom queryset with select_related for better performance"""
        return super().get_queryset(request).select_related('reviewed_by')
    
    def save_model(self, request, obj, form, change):
        """Custom save to track who reviewed the application"""
        if change and 'status' in form.changed_data:
            obj.reviewed_by = request.user
        super().save_model(request, obj, form, change)
