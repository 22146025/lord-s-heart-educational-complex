from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class AdmissionApplication(models.Model):
    """
    Model for storing pupil admission applications
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    
    # Pupil's Data
    surname = models.CharField(max_length=100, help_text="Surname in BLOCK LETTERS")
    first_name = models.CharField(max_length=100)
    other_names = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField()
    age = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(25)],
        help_text="Age at time of application"
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    place_of_birth = models.CharField(max_length=100)
    region_of_birth = models.CharField(max_length=100)
    home_town = models.CharField(max_length=100)
    region_of_home_town = models.CharField(max_length=100)
    last_school_attended = models.CharField(max_length=200, blank=True, null=True)
    location_of_last_school = models.CharField(max_length=200, blank=True, null=True)
    class_before_admission = models.CharField(max_length=50, help_text="Class/Stage before admission")
    religious_denomination = models.CharField(max_length=100, blank=True, null=True)
    hobbies = models.TextField(blank=True, null=True, help_text="Child's hobbies or interests")
    disability_or_allergy = models.TextField(blank=True, null=True, help_text="State any disability or allergy")
    
    # Parent/Guardian Data
    father_name = models.CharField(max_length=100, blank=True, null=True)
    mother_name = models.CharField(max_length=100, blank=True, null=True)
    father_occupation = models.CharField(max_length=100, blank=True, null=True)
    mother_occupation = models.CharField(max_length=100, blank=True, null=True)
    father_contact = models.CharField(max_length=20, blank=True, null=True)
    mother_contact = models.CharField(max_length=20, blank=True, null=True)
    father_email = models.EmailField(blank=True, null=True)
    mother_email = models.EmailField(blank=True, null=True)
    postal_address = models.TextField()
    place_of_residence = models.CharField(max_length=200)
    house_number = models.CharField(max_length=50, blank=True, null=True)
    
    # Application Status and Metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    application_date = models.DateTimeField(default=timezone.now)
    reviewed_date = models.DateTimeField(blank=True, null=True)
    reviewed_by = models.ForeignKey(
        'auth.User', 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True,
        related_name='reviewed_applications'
    )
    notes = models.TextField(blank=True, null=True, help_text="Internal notes for the application")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-application_date']
        verbose_name = 'Admission Application'
        verbose_name_plural = 'Admission Applications'
    
    def __str__(self):
        return f"{self.surname} {self.first_name} - {self.status}"
    
    def save(self, *args, **kwargs):
        # Auto-calculate age if not provided
        if not self.age and self.date_of_birth:
            from datetime import date
            today = date.today()
            self.age = today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        super().save(*args, **kwargs)
    
    @property
    def full_name(self):
        """Return the full name of the applicant"""
        names = [self.surname, self.first_name]
        if self.other_names:
            names.append(self.other_names)
        return ' '.join(names)
    
    @property
    def is_pending(self):
        """Check if application is pending"""
        return self.status == 'pending'
    
    @property
    def is_accepted(self):
        """Check if application is accepted"""
        return self.status == 'accepted'
    
    @property
    def is_rejected(self):
        """Check if application is rejected"""
        return self.status == 'rejected'
