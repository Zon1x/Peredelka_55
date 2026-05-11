from django.db import models

# Create your models here.
class SiteSettings(models.Model):
    # Основные настройки
    site_name = models.CharField(max_length=200, default='Peredelka55')
    company_name = models.CharField(max_length=200, default='Peredelka55')
    main_phone = models.CharField(max_length=30, default='+7 (983) 113-82-55')
    additional_phone = models.CharField(max_length=20, blank=True, null=True)
    main_email = models.EmailField(default='jeka_22.09.83@mail.ru')
    additional_email = models.EmailField(blank=True, null=True)
    address = models.CharField(
        max_length=255,
        default='г. Омск, ул. Рельсовая, д. 25',
    )
    working_hours = models.CharField(max_length=100, default='Пн-Пт: 9:00-18:00')

    company_legal_name = models.CharField(
        max_length=200,
        default='ИП Зимин Евгений Николаевич',
        verbose_name='ИП / наименование организации',
    )
    company_inn = models.CharField(
        max_length=20, blank=True, default='', verbose_name='ИНН'
    )
    company_ogrn = models.CharField(
        max_length=20, blank=True, default='', verbose_name='ОГРН / ОГРНИП'
    )
    company_rs = models.CharField(
        max_length=34,
        blank=True,
        default='',
        verbose_name='Расчётный счёт',
    )
    company_bank = models.CharField(
        max_length=255,
        blank=True,
        default='',
        verbose_name='Банк',
    )

    # Социальные сети
    vk_link = models.URLField(blank=True, null=True)
    telegram_link = models.URLField(blank=True, null=True)
    whatsapp_link = models.URLField(blank=True, null=True)
    show_social_icons = models.BooleanField(default=True)

    # SEO настройки
    default_meta_title = models.CharField(max_length=255, default='Переделка55 - Переоборудование спецтехники')
    default_meta_description = models.TextField(
        default='Омск: удлинение рамы, изготовление и монтаж еврофургона, подготовка к техосмотру, ремонт и восстановление рамы грузового транспорта. Ориентировочные цены и сроки — после осмотра.',
    )
    keywords = models.CharField(
        max_length=255,
        default='удлинение рамы, еврофургон, техосмотр, ремонт рамы, Омск, грузовой транспорт',
    )
    og_title = models.CharField(max_length=255, blank=True, null=True)
    og_description = models.TextField(blank=True, null=True)
    og_image = models.ImageField(upload_to='og_images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk and SiteSettings.objects.exists():
            # Если это новый объект и уже существует запись, обновляем существующую
            existing_settings = SiteSettings.objects.first()
            self.pk = existing_settings.pk
            kwargs.pop('force_insert', None)
        super(SiteSettings, self).save(*args, **kwargs)

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"


class Statistic(models.Model):
    projects_completed = models.PositiveIntegerField(
        default=1000,
        verbose_name="Количество выполненных проектов",
        help_text='По ТЗ: 1000 проектов в Омске',
    )
    years_of_experience = models.PositiveIntegerField(
        default=7,
        verbose_name="Годы опыта работы",
        help_text='По ТЗ: 7 лет',
    )
    satisfied_clients_percentage = models.PositiveIntegerField(default=97, verbose_name="Процент довольных клиентов")
    specialists_count = models.PositiveIntegerField(default=15, verbose_name="Количество специалистов")

    def save(self, *args, **kwargs):
        if not self.pk and Statistic.objects.exists():
            existing_stat = Statistic.objects.first()
            self.pk = existing_stat.pk
            kwargs.pop('force_insert', None)
        super(Statistic, self).save(*args, **kwargs)

    def __str__(self):
        return "Статистика компании"

    class Meta:
        verbose_name = "Статистика"
        verbose_name_plural = "Статистика"
