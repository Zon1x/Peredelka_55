from django.contrib import admin
from .models import SiteSettings, Statistic

# Register your models here.
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Основные настройки', {
            'fields': (
                'site_name',
                'company_name',
                'main_phone',
                'additional_phone',
                'main_email',
                'additional_email',
                'address',
                'working_hours',
            ),
        }),
        ('Реквизиты (для страницы «Контакты»)', {
            'fields': (
                'company_legal_name',
                'company_inn',
                'company_ogrn',
                'company_rs',
                'company_bank',
            ),
        }),
        ('Социальные сети', {
            'fields': ('vk_link', 'telegram_link', 'whatsapp_link', 'show_social_icons')
        }),
        ('SEO настройки', {
            'fields': ('default_meta_title', 'default_meta_description', 'keywords', 'og_title', 'og_description', 'og_image')
        }),
    )

    def has_add_permission(self, request):
        # Разрешить добавлять только если нет записей
        if self.model.objects.count() > 0:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        # Запретить удаление
        return False

@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ('projects_completed', 'years_of_experience', 'satisfied_clients_percentage', 'specialists_count')

    def has_add_permission(self, request):
        if self.model.objects.count() > 0:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False
