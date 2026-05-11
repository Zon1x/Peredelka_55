from django.test import TestCase, Client
from django.urls import reverse

from .constants import FOUR_CORE_SERVICE_NAMES
from .models import ServiceCategory, Service


class ServiceCategoryModelTest(TestCase):
    def setUp(self):
        ServiceCategory.objects.create(name="Category 1", ordering=1)
        ServiceCategory.objects.create(name="Category 2", ordering=2)

    def test_service_category_creation(self):
        category1 = ServiceCategory.objects.get(name="Category 1")
        self.assertEqual(category1.ordering, 1)

    def test_str_representation(self):
        category = ServiceCategory.objects.get(name="Category 1")
        self.assertEqual(str(category), "Category 1")


class ServiceModelTest(TestCase):
    def setUp(self):
        self.category = ServiceCategory.objects.create(name="Test Category")
        Service.objects.create(
            category=self.category,
            name="Тестовая карточка услуги",
            description="Test Description",
            price_from=99999.00,
            is_active=True,
        )

    def test_service_creation(self):
        service = Service.objects.get(name="Тестовая карточка услуги")
        self.assertEqual(service.category, self.category)
        self.assertEqual(float(service.price_from), 99999.00)

    def test_str_representation(self):
        service = Service.objects.get(name="Тестовая карточка услуги")
        self.assertEqual(str(service), "Тестовая карточка услуги")


class ServiceViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category_a = ServiceCategory.objects.create(name="Удлинение рамы", ordering=1)
        self.category_b = ServiceCategory.objects.create(name="Еврофургон", ordering=2)
        self.service1 = Service.objects.create(
            category=self.category_a,
            name="Удлинение рамы",
            description="Desc",
            price_from=100000.00,
            is_active=True,
        )
        self.service2 = Service.objects.create(
            category=self.category_b,
            name="Еврофургон",
            description="Desc",
            price_from=200000.00,
            is_active=True,
        )
        Service.objects.create(
            category=self.category_a,
            name="Старая услуга КМУ",
            description="Legacy",
            price_from=100.00,
            is_active=True,
        )

    def test_service_list_only_core_services(self):
        response = self.client.get(reverse("services:service_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Удлинение рамы")
        self.assertContains(response, "Еврофургон")
        self.assertNotContains(response, "КМУ")
        names = list(response.context["fixed_service_names"])
        self.assertEqual(names, list(FOUR_CORE_SERVICE_NAMES))

    def test_service_detail_view_core(self):
        response = self.client.get(reverse("services:service_detail", args=[self.service1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "services/service_detail.html")
