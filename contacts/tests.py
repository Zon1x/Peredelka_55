from django.test import TestCase, Client, override_settings
from django.urls import reverse
from .models import ContactRequest
from .forms import ContactForm
from services.models import Service, ServiceCategory
from unittest.mock import patch


class ContactRequestModelTest(TestCase):
    def setUp(self):
        self.category = ServiceCategory.objects.create(name="Test Category")
        self.service = Service.objects.create(
            category=self.category, name="Техосмотр", description="", price_from=5000.00
        )
        ContactRequest.objects.create(
            name="Alice",
            phone="111-222-3333",
            email="alice@example.com",
            service=self.service,
            message="Inquiry about service."
        )

    def test_contact_request_creation(self):
        request = ContactRequest.objects.get(name="Alice")
        self.assertEqual(request.email, "alice@example.com")
        self.assertEqual(request.service, self.service)

    def test_str_representation(self):
        request = ContactRequest.objects.get(name="Alice")
        self.assertIn("Alice", str(request))


class ContactFormTest(TestCase):
    def setUp(self):
        self.category = ServiceCategory.objects.create(name="Test Category")
        self.service = Service.objects.create(
            category=self.category, name="Техосмотр", description="", price_from=5000.00, is_active=True
        )

    def test_valid_form(self):
        data = {
            'name': 'Bob',
            'phone': '444-555-6666',
            'email': 'bob@example.com',
            'service': self.service.pk,
            'message': 'Hello'
        }
        form = ContactForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            'name': '',
            'phone': '444-555-6666',
            'email': 'bob@example.com',
            'service': self.service.pk,
            'message': 'Hello'
        }
        form = ContactForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)


class ContactViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = ServiceCategory.objects.create(name="Test Category")
        self.service = Service.objects.create(
            category=self.category, name="Техосмотр", description="", price_from=5000.00, is_active=True
        )

    def test_contact_form_view_get(self):
        response = self.client.get(reverse('contact_form'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contacts/contact_form.html')
        self.assertIsInstance(response.context['form'], ContactForm)

    @override_settings(SERVER_EMAIL='admin@test.example', DEFAULT_FROM_EMAIL='from@test.example')
    @patch('contacts.views.send_mail')
    def test_contact_form_view_post_valid(self, mock_send_mail):
        data = {
            'name': 'Charlie',
            'phone': '777-888-9999',
            'email': 'charlie@example.com',
            'vehicle_type': 'ГАЗель',
            'service': self.service.pk,
            'message': 'Interested in your services.'
        }
        response = self.client.post(reverse('contact_form'), data)
        self.assertEqual(response.status_code, 302)  # Redirects to success
        self.assertRedirects(response, reverse('contact_success'))
        self.assertEqual(ContactRequest.objects.count(), 1)
        mock_send_mail.assert_called_once()

    def test_contact_form_view_post_invalid(self):
        data = {'name': '', 'email': 'invalid-email', 'message': 'Hi'}
        response = self.client.post(reverse('contact_form'), data)
        self.assertEqual(response.status_code, 200)

    def test_contact_success_view(self):
        response = self.client.get(reverse('contact_success'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contacts/contact_success.html')
