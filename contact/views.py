from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Count
from datetime import datetime, timedelta

from .models import ContactMessage
from .serializers import (
    ContactMessageSerializer,
    ContactMessageListSerializer,
    ContactMessageUpdateSerializer
)


class ContactMessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing contact messages
    """
    queryset = ContactMessage.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['name', 'email', 'message']
    ordering_fields = ['created_at', 'name', 'email']
    ordering = ['-created_at']
    
    def get_permissions(self):
        """Set permissions based on action"""
        if self.action == 'create':
            permission_classes = [AllowAny]  # Public can submit contact forms
        else:
            permission_classes = [IsAdminUser]  # Only admins can view/manage
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return ContactMessageListSerializer
        elif self.action in ['update', 'partial_update']:
            return ContactMessageUpdateSerializer
        return ContactMessageSerializer
    
    def get_queryset(self):
        """Filter queryset based on user permissions"""
        if not self.request.user.is_staff:
            return ContactMessage.objects.none()
        return super().get_queryset()
    
    def perform_create(self, serializer):
        """Capture additional information when creating contact message"""
        # Get client IP address
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        
        # Get user agent
        user_agent = self.request.META.get('HTTP_USER_AGENT', '')
        
        serializer.save(ip_address=ip, user_agent=user_agent)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def statistics(self, request):
        """Get contact message statistics for admin dashboard"""
        total_messages = ContactMessage.objects.count()
        new_messages = ContactMessage.objects.filter(status='new').count()
        read_messages = ContactMessage.objects.filter(status='read').count()
        replied_messages = ContactMessage.objects.filter(status='replied').count()
        archived_messages = ContactMessage.objects.filter(status='archived').count()
        
        # Messages by status
        status_stats = ContactMessage.objects.values('status').annotate(
            count=Count('id')
        )
        
        # Recent messages (last 30 days)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_messages = ContactMessage.objects.filter(
            created_at__gte=thirty_days_ago
        ).count()
        
        # Messages by day (last 7 days)
        seven_days_ago = timezone.now() - timedelta(days=7)
        daily_stats = ContactMessage.objects.filter(
            created_at__gte=seven_days_ago
        ).extra(
            select={'day': 'date(created_at)'}
        ).values('day').annotate(count=Count('id')).order_by('day')
        
        return Response({
            'total_messages': total_messages,
            'new_messages': new_messages,
            'read_messages': read_messages,
            'replied_messages': replied_messages,
            'archived_messages': archived_messages,
            'recent_messages': recent_messages,
            'status_statistics': list(status_stats),
            'daily_statistics': list(daily_stats),
        })
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def new(self, request):
        """Get all new messages"""
        new_messages = ContactMessage.objects.filter(status='new')
        serializer = self.get_serializer(new_messages, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def mark_as_read(self, request, pk=None):
        """Mark a message as read"""
        message = self.get_object()
        message.mark_as_read()
        serializer = self.get_serializer(message)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def mark_as_replied(self, request, pk=None):
        """Mark a message as replied"""
        message = self.get_object()
        message.mark_as_replied()
        serializer = self.get_serializer(message)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def archive(self, request, pk=None):
        """Archive a message"""
        message = self.get_object()
        message.archive()
        serializer = self.get_serializer(message)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def export(self, request):
        """Export contact messages data"""
        messages = self.get_queryset()
        serializer = ContactMessageSerializer(messages, many=True)
        return Response(serializer.data)
