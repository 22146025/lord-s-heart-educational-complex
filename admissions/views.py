from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Count, Q
from datetime import datetime, timedelta

from .models import AdmissionApplication
from .serializers import (
    AdmissionApplicationSerializer,
    AdmissionApplicationListSerializer,
    AdmissionApplicationUpdateSerializer
)


class AdmissionApplicationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing admission applications
    """
    queryset = AdmissionApplication.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'gender', 'class_before_admission']
    search_fields = ['surname', 'first_name', 'other_names', 'father_name', 'mother_name']
    ordering_fields = ['application_date', 'created_at', 'surname', 'first_name']
    ordering = ['-application_date']
    
    def get_permissions(self):
        """Set permissions based on action"""
        if self.action in ['create', 'list']:
            permission_classes = [AllowAny]  # Public can submit and view list
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]  # Only admins can modify
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return AdmissionApplicationListSerializer
        elif self.action in ['update', 'partial_update']:
            return AdmissionApplicationUpdateSerializer
        return AdmissionApplicationSerializer
    
    def get_queryset(self):
        """Filter queryset based on user permissions"""
        queryset = super().get_queryset()
        
        # If user is not admin, only show their own applications or public list
        if not self.request.user.is_staff:
            # For public users, only show basic info in list view
            if self.action == 'list':
                return queryset.filter(status__in=['accepted', 'rejected']).only(
                    'id', 'surname', 'first_name', 'status', 'application_date'
                )
            else:
                # For other actions, return empty queryset for non-admin users
                return AdmissionApplication.objects.none()
        
        return queryset
    
    def perform_create(self, serializer):
        """Set application date when creating"""
        serializer.save(application_date=timezone.now())
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def statistics(self, request):
        """Get admission statistics for admin dashboard"""
        total_applications = AdmissionApplication.objects.count()
        pending_applications = AdmissionApplication.objects.filter(status='pending').count()
        accepted_applications = AdmissionApplication.objects.filter(status='accepted').count()
        rejected_applications = AdmissionApplication.objects.filter(status='rejected').count()
        
        # Applications by gender
        gender_stats = AdmissionApplication.objects.values('gender').annotate(
            count=Count('id')
        )
        
        # Applications by class
        class_stats = AdmissionApplication.objects.values('class_before_admission').annotate(
            count=Count('id')
        )
        
        # Recent applications (last 30 days)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_applications = AdmissionApplication.objects.filter(
            application_date__gte=thirty_days_ago
        ).count()
        
        return Response({
            'total_applications': total_applications,
            'pending_applications': pending_applications,
            'accepted_applications': accepted_applications,
            'rejected_applications': rejected_applications,
            'recent_applications': recent_applications,
            'gender_statistics': list(gender_stats),
            'class_statistics': list(class_stats),
        })
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def pending(self, request):
        """Get all pending applications"""
        pending_applications = AdmissionApplication.objects.filter(status='pending')
        serializer = self.get_serializer(pending_applications, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def approve(self, request, pk=None):
        """Approve an application"""
        application = self.get_object()
        application.status = 'accepted'
        application.reviewed_date = timezone.now()
        application.reviewed_by = request.user
        application.save()
        
        serializer = self.get_serializer(application)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def reject(self, request, pk=None):
        """Reject an application"""
        application = self.get_object()
        application.status = 'rejected'
        application.reviewed_date = timezone.now()
        application.reviewed_by = request.user
        application.save()
        
        serializer = self.get_serializer(application)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def export(self, request):
        """Export applications data (basic implementation)"""
        applications = self.get_queryset()
        serializer = AdmissionApplicationSerializer(applications, many=True)
        return Response(serializer.data)
