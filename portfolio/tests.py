from django.test import TestCase, Client
from django.urls import reverse
from datetime import date
from .models import PortfolioCategory, PortfolioItem
from services.models import Service, ServiceCategory


class PortfolioCategoryModelTest(TestCase):
    def test_category_creation(self):
        category = PortfolioCategory.objects.create(
            name="Грузовики", slug="gruzoviki", ordering=1
        )
        self.assertEqual(str(category), "Грузовики")
        self.assertEqual(category.slug, "gruzoviki")


class PortfolioItemModelTest(TestCase):
    def setUp(self):
        self.portfolio_category = PortfolioCategory.objects.create(
            name="Trucks", slug="trucks"
        )
        self.service_category = ServiceCategory.objects.create(name="Test Service Category")
        self.service = Service.objects.create(
            category=self.service_category,
            name="Used Service",
            description="",
            price_from=100.00
        )
        self.portfolio_item = PortfolioItem.objects.create(
            category=self.portfolio_category,
            title="Truck Conversion",
            description="Detailed description of truck conversion.",
            before_image='portfolio/before/test_before.jpg',
            after_image='portfolio/after/test_after.jpg',
            completion_date=date(2023, 1, 1)
        )
        self.portfolio_item.services_used.add(self.service)

    def test_portfolio_item_creation(self):
        item = PortfolioItem.objects.get(title="Truck Conversion")
        self.assertEqual(item.category, self.portfolio_category)
        self.assertEqual(item.services_used.count(), 1)

    def test_str_representation(self):
        item = PortfolioItem.objects.get(title="Truck Conversion")
        self.assertEqual(str(item), "Truck Conversion")


class PortfolioViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.service_category = ServiceCategory.objects.create(name="Service Cat")
        self.service = Service.objects.create(
            category=self.service_category,
            name="Service Used",
            description="",
            price_from=100.00
        )

        self.cat_trucks = PortfolioCategory.objects.create(
            name="Trucks", slug="trucks"
        )
        self.cat_vans = PortfolioCategory.objects.create(
            name="Vans", slug="vans"
        )

        self.item1 = PortfolioItem.objects.create(
            category=self.cat_trucks,
            title="Truck Project A",
            description="Desc A",
            before_image='portfolio/before/a.jpg',
            after_image='portfolio/after/a.jpg',
            completion_date=date(2023, 3, 1)
        )
        self.item1.services_used.add(self.service)

        self.item2 = PortfolioItem.objects.create(
            category=self.cat_vans,
            title="Van Project B",
            description="Desc B",
            before_image='portfolio/before/b.jpg',
            after_image='portfolio/after/b.jpg',
            completion_date=date(2023, 2, 1)
        )

    def test_portfolio_list_view(self):
        response = self.client.get(reverse('portfolio:portfolio_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/portfolio_list.html')
        self.assertContains(response, "Truck Project A")
        self.assertContains(response, "Van Project B")

    def test_portfolio_list_filter_unknown_slug_returns_404(self):
        response = self.client.get(
            reverse('portfolio:portfolio_list_by_category', args=['trucks'])
        )
        self.assertEqual(response.status_code, 404)

    def test_portfolio_list_filter_by_allowed_slug(self):
        euro = PortfolioCategory.objects.get(slug="evrofurgon")
        item_ev = PortfolioItem.objects.create(
            category=euro,
            title="Evro Demo",
            description="Euro body",
            completion_date=date(2024, 1, 15),
        )
        response = self.client.get(
            reverse('portfolio:portfolio_list_by_category', args=["evrofurgon"])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Evro Demo")

        response_all = self.client.get(reverse('portfolio:portfolio_list'))
        self.assertEqual(response_all.status_code, 200)
        self.assertContains(response_all, "Truck Project A")
        self.assertContains(response_all, "Evro Demo")

    def test_portfolio_detail_view(self):
        response = self.client.get(
            reverse('portfolio:portfolio_detail', args=[self.item1.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/portfolio_detail.html')
        self.assertContains(response, "Truck Project A")
        self.assertContains(response, "Desc A")
