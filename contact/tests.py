from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import ContactMessage


class ContactMessageModelTest(TestCase):
    """Test cases for ContactMessage model"""
    
    def setUp(self):
        """Set up test data"""
        self.message_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'message': 'This is a test message for the contact form.',
            'ip_address': '127.0.0.1',
            'user_agent': 'Mozilla/5.0 Test Browser',
        }
    
    def test_create_contact_message(self):
        """Test creating a contact message"""
        message = ContactMessage.objects.create(**self.message_data)
        self.assertEqual(message.name, 'John Doe')
        self.assertEqual(message.email, 'john@example.com')
        self.assertEqual(message.status, 'new')
        self.assertIsNotNone(message.created_at)
    
    def test_status_properties(self):
        """Test status properties"""
        message = ContactMessage.objects.create(**self.message_data)
        
        # Test new status
        self.assertTrue(message.is_new)
        self.assertFalse(message.is_read)
        self.assertFalse(message.is_replied)
        
        # Test read status
        message.mark_as_read()
        self.assertFalse(message.is_new)
        self.assertTrue(message.is_read)
        self.assertFalse(message.is_replied)
        
        # Test replied status
        message.mark_as_replied()
        self.assertFalse(message.is_new)
        self.assertTrue(message.is_read)
        self.assertTrue(message.is_replied)
    
    def test_mark_as_read(self):
        """Test mark_as_read method"""
        message = ContactMessage.objects.create(**self.message_data)
        self.assertEqual(message.status, 'new')
        
        message.mark_as_read()
        message.refresh_from_db()
        self.assertEqual(message.status, 'read')
        self.assertIsNotNone(message.read_at)
    
    def test_mark_as_replied(self):
        """Test mark_as_replied method"""
        message = ContactMessage.objects.create(**self.message_data)
        
        message.mark_as_replied()
        message.refresh_from_db()
        self.assertEqual(message.status, 'replied')
        self.assertIsNotNone(message.replied_at)
    
    def test_archive(self):
        """Test archive method"""
        message = ContactMessage.objects.create(**self.message_data)
        
        message.archive()
        message.refresh_from_db()
        self.assertEqual(message.status, 'archived')


class ContactMessageAPITest(APITestCase):
    """Test cases for ContactMessage API"""
    
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
        
        self.message_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'message': 'This is a test message for the contact form.',
        }
    
    def test_create_message_public_access(self):
        """Test that public users can create contact messages"""
        url = reverse('contact-list')
        response = self.client.post(url, self.message_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContactMessage.objects.count(), 1)
        
        # Check that IP and user agent were captured
        message = ContactMessage.objects.first()
        self.assertIsNotNone(message.ip_address)
    
    def test_list_messages_admin_only(self):
        """Test that only admins can list messages"""
        # Create a message
        message = ContactMessage.objects.create(**self.message_data)
        
        url = reverse('contact-list')
        
        # Test without authentication
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Test with regular user
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Test with admin user
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_message_validation(self):
        """Test message validation"""
        url = reverse('contact-list')
        
        # Test short name
        invalid_data = self.message_data.copy()
        invalid_data['name'] = 'A'
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test short message
        invalid_data = self.message_data.copy()
        invalid_data['message'] = 'Short'
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test invalid email
        invalid_data = self.message_data.copy()
        invalid_data['email'] = 'invalid-email'
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_message_statistics(self):
        """Test message statistics endpoint"""
        # Create some messages
        ContactMessage.objects.create(**self.message_data)
        
        data2 = self.message_data.copy()
        data2['name'] = 'Jane Smith'
        data2['email'] = 'jane@example.com'
        ContactMessage.objects.create(**data2)
        
        url = reverse('contact-statistics')
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_messages'], 2)
        self.assertEqual(response.data['new_messages'], 2)
    
    def test_mark_as_read_action(self):
        """Test mark_as_read action"""
        message = ContactMessage.objects.create(**self.message_data)
        
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('contact-mark-as-read', args=[message.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        message.refresh_from_db()
        self.assertEqual(message.status, 'read')
        self.assertIsNotNone(message.read_at)
    
    def test_mark_as_replied_action(self):
        """Test mark_as_replied action"""
        message = ContactMessage.objects.create(**self.message_data)
        
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('contact-mark-as-replied', args=[message.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        message.refresh_from_db()
        self.assertEqual(message.status, 'replied')
        self.assertIsNotNone(message.replied_at)
    
    def test_archive_action(self):
        """Test archive action"""
        message = ContactMessage.objects.create(**self.message_data)
        
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('contact-archive', args=[message.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        message.refresh_from_db()
        self.assertEqual(message.status, 'archived')
    
    def test_new_messages_endpoint(self):
        """Test new messages endpoint"""
        # Create messages with different statuses
        ContactMessage.objects.create(**self.message_data)  # new
        
        data2 = self.message_data.copy()
        data2['name'] = 'Jane Smith'
        data2['email'] = 'jane@example.com'
        message2 = ContactMessage.objects.create(**data2)
        message2.mark_as_read()  # read
        
        url = reverse('contact-new')
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Only new message
