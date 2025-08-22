from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import date, timedelta
from .models import AdmissionApplication


class AdmissionApplicationModelTest(TestCase):
    """Test cases for AdmissionApplication model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testadmin',
            email='admin@test.com',
            password='testpass123'
        )
        self.user.is_staff = True
        self.user.save()
        
        self.application_data = {
            'surname': 'DOE',
            'first_name': 'John',
            'other_names': 'Michael',
            'date_of_birth': date(2015, 5, 15),
            'age': 8,
            'gender': 'male',
            'place_of_birth': 'Accra',
            'region_of_birth': 'Greater Accra',
            'home_town': 'Kumasi',
            'region_of_home_town': 'Ashanti',
            'last_school_attended': 'Test Primary School',
            'location_of_last_school': 'Accra',
            'class_before_admission': 'Class 2',
            'religious_denomination': 'Christian',
            'hobbies': 'Reading, Swimming',
            'disability_or_allergy': 'None',
            'father_name': 'John Doe Sr.',
            'mother_name': 'Jane Doe',
            'father_occupation': 'Engineer',
            'mother_occupation': 'Teacher',
            'father_contact': '+233123456789',
            'mother_contact': '+233987654321',
            'father_email': 'father@test.com',
            'mother_email': 'mother@test.com',
            'postal_address': 'P.O. Box 123, Accra',
            'place_of_residence': 'Accra',
            'house_number': 'A123',
        }
    
    def test_create_admission_application(self):
        """Test creating an admission application"""
        application = AdmissionApplication.objects.create(**self.application_data)
        self.assertEqual(application.surname, 'DOE')
        self.assertEqual(application.first_name, 'John')
        self.assertEqual(application.status, 'pending')
        self.assertIsNotNone(application.application_date)
    
    def test_full_name_property(self):
        """Test the full_name property"""
        application = AdmissionApplication.objects.create(**self.application_data)
        expected_name = "DOE John Michael"
        self.assertEqual(application.full_name, expected_name)
    
    def test_status_properties(self):
        """Test status properties"""
        application = AdmissionApplication.objects.create(**self.application_data)
        
        # Test pending status
        self.assertTrue(application.is_pending)
        self.assertFalse(application.is_accepted)
        self.assertFalse(application.is_rejected)
        
        # Test accepted status
        application.status = 'accepted'
        application.save()
        self.assertFalse(application.is_pending)
        self.assertTrue(application.is_accepted)
        self.assertFalse(application.is_rejected)
        
        # Test rejected status
        application.status = 'rejected'
        application.save()
        self.assertFalse(application.is_pending)
        self.assertFalse(application.is_accepted)
        self.assertTrue(application.is_rejected)
    
    def test_auto_calculate_age(self):
        """Test automatic age calculation"""
        # Create application without age
        data_without_age = self.application_data.copy()
        data_without_age.pop('age')
        data_without_age['date_of_birth'] = date.today() - timedelta(days=365*8)  # 8 years ago
        
        application = AdmissionApplication.objects.create(**data_without_age)
        self.assertEqual(application.age, 8)


class AdmissionApplicationAPITest(APITestCase):
    """Test cases for AdmissionApplication API"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='adminpass123'
        )
        self.admin_user.is_staff = True
        self.admin_user.save()
        
        self.regular_user = User.objects.create_user(
            username='user',
            email='user@test.com',
            password='userpass123'
        )
        
        self.application_data = {
            'surname': 'DOE',
            'first_name': 'John',
            'other_names': 'Michael',
            'date_of_birth': '2015-05-15',
            'age': 8,
            'gender': 'male',
            'place_of_birth': 'Accra',
            'region_of_birth': 'Greater Accra',
            'home_town': 'Kumasi',
            'region_of_home_town': 'Ashanti',
            'last_school_attended': 'Test Primary School',
            'location_of_last_school': 'Accra',
            'class_before_admission': 'Class 2',
            'religious_denomination': 'Christian',
            'hobbies': 'Reading, Swimming',
            'disability_or_allergy': 'None',
            'father_name': 'John Doe Sr.',
            'mother_name': 'Jane Doe',
            'father_occupation': 'Engineer',
            'mother_occupation': 'Teacher',
            'father_contact': '+233123456789',
            'mother_contact': '+233987654321',
            'father_email': 'father@test.com',
            'mother_email': 'mother@test.com',
            'postal_address': 'P.O. Box 123, Accra',
            'place_of_residence': 'Accra',
            'house_number': 'A123',
        }
    
    def test_create_application_public_access(self):
        """Test that public users can create applications"""
        url = reverse('admission-list')
        response = self.client.post(url, self.application_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AdmissionApplication.objects.count(), 1)
    
    def test_list_applications_admin_access(self):
        """Test that only admins can list applications"""
        # Create an application
        application = AdmissionApplication.objects.create(**self.application_data)
        
        url = reverse('admission-list')
        
        # Test without authentication
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test with regular user
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test with admin user
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_application_admin_only(self):
        """Test that only admins can update applications"""
        application = AdmissionApplication.objects.create(**self.application_data)
        url = reverse('admission-detail', args=[application.id])
        update_data = {'status': 'accepted'}
        
        # Test without authentication
        response = self.client.patch(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Test with regular user
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.patch(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Test with admin user
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.patch(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'accepted')
    
    def test_application_validation(self):
        """Test application validation"""
        url = reverse('admission-list')
        
        # Test invalid date of birth (future date)
        invalid_data = self.application_data.copy()
        invalid_data['date_of_birth'] = '2030-01-01'
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test invalid age
        invalid_data = self.application_data.copy()
        invalid_data['age'] = 30
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test missing parent contact
        invalid_data = self.application_data.copy()
        invalid_data['father_contact'] = ''
        invalid_data['mother_contact'] = ''
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_application_statistics(self):
        """Test application statistics endpoint"""
        # Create some applications
        AdmissionApplication.objects.create(**self.application_data)
        
        data2 = self.application_data.copy()
        data2['surname'] = 'SMITH'
        data2['first_name'] = 'Jane'
        AdmissionApplication.objects.create(**data2)
        
        url = reverse('admission-statistics')
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_applications'], 2)
        self.assertEqual(response.data['pending_applications'], 2)
    
    def test_approve_reject_actions(self):
        """Test approve and reject actions"""
        application = AdmissionApplication.objects.create(**self.application_data)
        
        self.client.force_authenticate(user=self.admin_user)
        
        # Test approve action
        url = reverse('admission-approve', args=[application.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        application.refresh_from_db()
        self.assertEqual(application.status, 'accepted')
        self.assertIsNotNone(application.reviewed_date)
        self.assertEqual(application.reviewed_by, self.admin_user)
        
        # Test reject action
        application.status = 'pending'
        application.save()
        
        url = reverse('admission-reject', args=[application.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        application.refresh_from_db()
        self.assertEqual(application.status, 'rejected')
