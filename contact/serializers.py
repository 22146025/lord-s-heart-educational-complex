from rest_framework import serializers
from .models import ContactMessage


class ContactMessageSerializer(serializers.ModelSerializer):
    """Serializer for ContactMessage model"""
    
    class Meta:
        model = ContactMessage
        fields = '__all__'
        read_only_fields = ['status', 'ip_address', 'user_agent', 'created_at', 'updated_at', 'read_at', 'replied_at']
    
    def validate_name(self, value):
        """Validate name field"""
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters long.")
        return value.strip()
    
    def validate_message(self, value):
        """Validate message field"""
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Message must be at least 10 characters long.")
        return value.strip()


class ContactMessageListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing contact messages (admin only)"""
    
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'status', 'created_at', 'is_new', 'is_read', 'is_replied']


class ContactMessageUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating contact message status (admin only)"""
    
    class Meta:
        model = ContactMessage
        fields = ['status']
    
    def update(self, instance, validated_data):
        """Update status and handle related timestamps"""
        new_status = validated_data.get('status')
        
        if new_status == 'read' and instance.status == 'new':
            instance.mark_as_read()
        elif new_status == 'replied':
            instance.mark_as_replied()
        elif new_status == 'archived':
            instance.archive()
        else:
            instance.status = new_status
            instance.save()
        
        return instance
