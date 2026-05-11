from django.contrib import admin
from .models import ServiceCategory, Service

# Register your models here.
@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'ordering', 'icon')
    list_editable = ('ordering',)
    search_fields = ('name',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price_from', 'is_active', 'specialist_visit')
    list_filter = ('category', 'is_active', 'specialist_visit')
    search_fields = ('name', 'description', 'terms', 'guarantee', 'work_process')
    list_editable = ('is_active',)
    fieldsets = (
        (None, {
            'fields': ('category', 'name', 'description', 'price_from', 'image', 'is_active')
        }),
        ('Детали услуги', {
            'fields': ('terms', 'guarantee', 'specialist_visit', 'work_process'),
            'classes': ('collapse',),
        }),
    )
