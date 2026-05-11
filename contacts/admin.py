from django.contrib import admin
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactRequest


@admin.action(description='Mark selected as processed')
def make_processed(modeladmin, request, queryset):
    queryset.update(is_processed=True)

@admin.action(description='Send email confirmation to client')
def send_confirmation_email(modeladmin, request, queryset):
    for contact_request in queryset:
        if contact_request.email:
            subject = f'Заявка с сайта {getattr(settings, "SITE_NAME", "Peredelka55")}'
            html_message = render_to_string('contacts/emails/client_confirmation.html', {'contact_request': contact_request, 'site_settings': modeladmin.site_settings})
            plain_message = f'Dear {contact_request.name},\n\nThank you for your contact request. We will get back to you shortly.'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [contact_request.email]
            send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
    modeladmin.message_user(request, 'Confirmation emails sent to selected clients.')

@admin.action(description='Export selected contact requests to CSV')
def export_as_csv(modeladmin, request, queryset):
    import csv
    from django.http import HttpResponse

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="contact_requests.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Vehicle', 'Phone', 'Email', 'Service', 'Message', 'Admin Comment', 'Created At', 'Processed'])

    for obj in queryset:
        writer.writerow([obj.name, obj.vehicle_type, obj.phone, obj.email, obj.service if obj.service else '', obj.message, obj.admin_comment, obj.created_at.strftime("%Y-%m-%d %H:%M"), obj.is_processed])

    return response


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'vehicle_type', 'phone', 'email', 'service', 'created_at', 'is_processed')
    list_filter = ('is_processed', 'service', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message', 'admin_comment', 'vehicle_type')
    list_editable = ('is_processed',)
    readonly_fields = ('created_at',)
    fields = (
        'name',
        'vehicle_type',
        'phone',
        'email',
        'service',
        'message',
        'admin_comment',
        'is_processed',
        'created_at',
    )
    actions = [make_processed, send_confirmation_email, export_as_csv]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields['admin_comment'].widget.attrs['readonly'] = True
        return form

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Здесь можно добавить логику для отправки уведомлений или других действий после сохранения

    def get_site_settings(self):
        from core.models import SiteSettings
        try:
            return SiteSettings.objects.get()
        except SiteSettings.DoesNotExist:
            return None

    @property
    def site_settings(self):
        return self.get_site_settings()
