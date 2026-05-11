from django.db import models
from services.models import Service
from django.utils import timezone

# Create your models here.

class PortfolioCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Слаг")
    description = models.TextField(blank=True, verbose_name="Описание категории")
    ordering = models.PositiveIntegerField(default=0, verbose_name="Порядок отображения")

    class Meta:
        verbose_name = "Категория портфолио"
        verbose_name_plural = "Категории портфолио"
        ordering = ['ordering', 'name']

    def __str__(self):
        return self.name


class PortfolioItem(models.Model):
    category = models.ForeignKey(PortfolioCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='portfolio_items', verbose_name="Категория техники")
    title = models.CharField(max_length=200, verbose_name="Название проекта")
    chassis_type = models.CharField(max_length=200, blank=True, verbose_name="Тип шасси")
    description = models.TextField(verbose_name="Описание проекта")
    equipment_summary = models.TextField(blank=True, verbose_name="Установленное оборудование")
    price_display = models.CharField(
        max_length=120,
        blank=True,
        verbose_name="Цена / диапазон",
        help_text='Например: от 450 000 ₽ или «индивидуальный расчёт»',
    )
    before_image = models.ImageField(
        upload_to='portfolio/before/',
        blank=True,
        null=True,
        verbose_name="Фото до",
    )
    after_image = models.ImageField(
        upload_to='portfolio/after/',
        blank=True,
        null=True,
        verbose_name="Фото после",
    )
    completion_date = models.DateField(verbose_name="Дата завершения")
    services_used = models.ManyToManyField(Service, blank=True, verbose_name="Использованные услуги")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")

    class Meta:
        verbose_name = "Элемент портфолио"
        verbose_name_plural = "Портфолио"
        ordering = ['completion_date']

    def __str__(self):
        return self.title
