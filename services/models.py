from django.db import models

# Create your models here.

class ServiceCategory(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название категории")
    description = models.TextField(blank=True, verbose_name="Описание категории")
    icon = models.CharField(max_length=50, blank=True, verbose_name="Иконка (Font Awesome)")
    ordering = models.PositiveIntegerField(default=0, verbose_name="Порядок отображения")

    class Meta:
        verbose_name = "Категория услуги"
        verbose_name_plural = "Категории услуг"
        ordering = ['ordering', 'name']

    def __str__(self):
        return self.name

class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services', verbose_name="Категория")
    name = models.CharField(max_length=200, verbose_name="Название услуги")
    description = models.TextField(verbose_name="Описание услуги")
    price_from = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Цена от")
    terms = models.TextField(blank=True, verbose_name="Сроки выполнения")
    guarantee = models.TextField(blank=True, verbose_name="Гарантия")
    specialist_visit = models.BooleanField(default=False, verbose_name="Возможен выезд специалиста")
    work_process = models.TextField(blank=True, verbose_name="Процесс работы")
    image = models.ImageField(upload_to='services/', blank=True, null=True, verbose_name="Изображение")
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ['name']

    def __str__(self):
        return self.name