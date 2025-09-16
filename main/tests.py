from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import ContactSubmission
import json

class ContactFormTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.contact_url = reverse('main:contact')
        
    def test_contact_form_get(self):
        """Test that the contact form page loads correctly"""
        response = self.client.get(self.contact_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Send Me a Message')
        
    def test_contact_form_post_valid_data(self):
        """Test submitting the contact form with valid data"""
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message.'
        }
        
        # First get the form to get CSRF token
        response = self.client.get(self.contact_url)
        self.assertEqual(response.status_code, 200)
        
        # Then submit the form
        response = self.client.post(self.contact_url, data)
        self.assertEqual(response.status_code, 200)
        
        # Check that the contact submission was saved
        submissions = ContactSubmission.objects.filter(email='john@example.com')
        self.assertEqual(submissions.count(), 1)
        
        submission = submissions.first()
        self.assertEqual(submission.name, 'John Doe')
        self.assertEqual(submission.subject, 'Test Subject')
        
    def test_contact_form_ajax_post_valid_data(self):
        """Test submitting the contact form via AJAX with valid data"""
        data = {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'subject': 'AJAX Test Subject',
            'message': 'This is an AJAX test message.'
        }
        
        response = self.client.post(
            self.contact_url,
            json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['message'], 'Thank you for your message! I will get back to you soon.')
        
        # Check that the contact submission was saved
        submissions = ContactSubmission.objects.filter(email='jane@example.com')
        self.assertEqual(submissions.count(), 1)