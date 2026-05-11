from django.contrib import admin
from .models import Promotion, PromotionReviewSubmission


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'bonus_summary', 'is_active', 'start_date', 'end_date', 'ordering')
    list_filter = ('is_active',)
    search_fields = ('title', 'description', 'teaser')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_active', 'ordering')


@admin.register(PromotionReviewSubmission)
class PromotionReviewSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'promotion', 'review_url', 'created_at', 'is_processed')
    list_filter = ('is_processed', 'promotion')
    search_fields = ('name', 'phone', 'review_url')
    list_editable = ('is_processed',)
    readonly_fields = ('created_at',)
