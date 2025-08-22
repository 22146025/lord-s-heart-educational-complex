from rest_framework import serializers
from .models import AdmissionApplication
from django.utils import timezone


class AdmissionApplicationSerializer(serializers.ModelSerializer):
    """Serializer for AdmissionApplication model"""
    
    full_name = serializers.ReadOnlyField()
    is_pending = serializers.ReadOnlyField()
    is_accepted = serializers.ReadOnlyField()
    is_rejected = serializers.ReadOnlyField()
    
    class Meta:
        model = AdmissionApplication
        fields = '__all__'
        read_only_fields = ['application_date', 'reviewed_date', 'reviewed_by', 'created_at', 'updated_at']
    
    def validate_date_of_birth(self, value):
        """Validate date of birth is not in the future"""
        if value > timezone.now().date():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return value
    
    def validate_age(self, value):
        """Validate age is reasonable for school admission"""
        if value < 1 or value > 25:
            raise serializers.ValidationError("Age must be between 1 and 25 years.")
        return value
    
    def validate(self, data):
        """Custom validation for the entire application"""
        # Ensure at least one parent contact is provided
        father_contact = data.get('father_contact')
        mother_contact = data.get('mother_contact')
        
        if not father_contact and not mother_contact:
            raise serializers.ValidationError(
                "At least one parent contact number must be provided."
            )
        
        # Validate email format if provided
        father_email = data.get('father_email')
        mother_email = data.get('mother_email')
        
        if father_email and '@' not in father_email:
            raise serializers.ValidationError("Father's email must be a valid email address.")
        
        if mother_email and '@' not in mother_email:
            raise serializers.ValidationError("Mother's email must be a valid email address.")
        
        return data


class AdmissionApplicationListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing applications"""
    
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = AdmissionApplication
        fields = [
            'id', 'surname', 'first_name', 'full_name', 'age', 'gender',
            'class_before_admission', 'status', 'application_date', 'created_at'
        ]


class AdmissionApplicationUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating application status (admin only)"""
    
    class Meta:
        model = AdmissionApplication
        fields = ['status', 'notes', 'reviewed_date']
        read_only_fields = ['reviewed_date']
    
    def update(self, instance, validated_data):
        """Update the application and set reviewed date"""
        if 'status' in validated_data and validated_data['status'] != instance.status:
            validated_data['reviewed_date'] = timezone.now()
            validated_data['reviewed_by'] = self.context['request'].user
        
        return super().update(instance, validated_data)
