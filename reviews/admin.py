from django.contrib import admin
from .models import Review

# Register your models here.
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'service_type', 'rating', 'is_published', 'created_at')
    list_filter = ('is_published', 'rating', 'service_type', 'created_at')
    search_fields = ('author_name', 'text')
    list_editable = ('is_published',)
    readonly_fields = ('created_at',)
