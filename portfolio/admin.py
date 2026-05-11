from django.contrib import admin
from .models import PortfolioCategory, PortfolioItem

@admin.register(PortfolioCategory)
class PortfolioCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'ordering')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('ordering',)

@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'chassis_type', 'price_display', 'completion_date', 'updated_at')
    list_filter = ('category', 'completion_date', 'services_used')
    search_fields = ('title', 'description', 'chassis_type', 'equipment_summary', 'price_display')
    filter_horizontal = ('services_used',)
    readonly_fields = ('date_created', 'updated_at')
    fieldsets = (
        (None, {'fields': ('category', 'title', 'chassis_type', 'description', 'equipment_summary', 'price_display')}),
        ('Медиа и даты', {'fields': ('before_image', 'after_image', 'completion_date', 'services_used')}),
        ('Служебное', {'fields': ('date_created', 'updated_at'), 'classes': ('collapse',)}),
    )
