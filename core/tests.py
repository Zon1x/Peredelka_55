from django.test import TestCase, Client
from django.urls import reverse

from .models import SiteSettings, Statistic
from .forms import VehicleConstructorForm
from services.models import Service, ServiceCategory


class SiteSettingsModelTest(TestCase):
    def setUp(self):
        SiteSettings.objects.create(
            site_name="Test Site",
            company_name="Test Company",
            main_phone="+123456789",
            main_email="test@example.com",
            address="123 Test St",
            working_hours="Mon-Fri 9-5",
        )

    def test_site_settings_creation(self):
        settings = SiteSettings.objects.get(pk=1)
        self.assertEqual(settings.site_name, "Test Site")
        self.assertEqual(settings.company_name, "Test Company")

    def test_str_representation(self):
        settings = SiteSettings.objects.get(pk=1)
        self.assertEqual(str(settings), "Test Site")

    def test_singleton_behavior(self):
        """Проверяем, что нельзя создать вторую запись — она перезаписывает первую."""
        SiteSettings.objects.create(
            site_name="Updated Site",
            company_name="Updated Company",
            main_phone="+987654321",
            main_email="updated@example.com",
            address="456 Updated St",
            working_hours="Mon-Sat 10-6",
        )
        self.assertEqual(SiteSettings.objects.count(), 1)
        settings = SiteSettings.objects.first()
        self.assertEqual(settings.site_name, "Updated Site")


class StatisticModelTest(TestCase):
    def test_statistic_creation(self):
        stat = Statistic.objects.create(
            projects_completed=100,
            years_of_experience=10,
            satisfied_clients_percentage=98,
            specialists_count=15,
        )
        self.assertEqual(stat.projects_completed, 100)
        self.assertEqual(str(stat), "Статистика компании")


class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        SiteSettings.objects.create(
            site_name="Test Site",
            company_name="Test Company",
            main_phone="+123456789",
            main_email="test@example.com",
            address="123 Test St",
            working_hours="Mon-Fri 9-5",
        )
        self.category = ServiceCategory.objects.create(name="Test Category")
        self.service_teh = Service.objects.create(
            category=self.category,
            name="Техосмотр",
            description="Desc 1",
            price_from=5000.00,
            is_active=True,
        )

    def test_home_view_get(self):
        response = self.client.get(reverse("core:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertIsInstance(response.context["constructor_form"], VehicleConstructorForm)

    def test_home_view_constructor_post(self):
        response = self.client.post(
            reverse("core:index"),
            {
                "submit": "constructor",
                "chassis": "medium",
                "service": "Техосмотр",
                "workload": "extended",
                "euro_body_length": "",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertAlmostEqual(response.context["estimated_cost"], 6439.5, places=1)
        self.assertEqual(response.context["selected_service"].name, "Техосмотр")
