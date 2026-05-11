from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .forms import ContactForm
from .models import ContactRequest


def notify_new_contact_request(contact_request, request=None):
    """Уведомление администратора о новой заявке (полная форма или быстрая с главной)."""
    subject = f'Новая заявка с сайта: {contact_request.name or "без имени"}'
    html_message = render_to_string(
        'contacts/emails/contact_notification.html',
        {'contact_request': contact_request, 'request': request},
    )
    plain_message = (
        f'Новая заявка.\n'
        f'Имя: {contact_request.name}\n'
        f'Телефон: {contact_request.phone}\n'
        f'Email: {contact_request.email}\n'
        f'Услуга: {contact_request.service}\n'
        f'Тип авто/услуга: {contact_request.vehicle_type}\n'
        f'Сообщение: {contact_request.message}'
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [settings.SERVER_EMAIL] if settings.SERVER_EMAIL else []

    if not recipient_list or not from_email:
        return
    try:
        send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
    except Exception:
        pass


def contact_form(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_request = form.save()
            notify_new_contact_request(contact_request, request=request)
            return redirect('contact_success')
    else:
        form = ContactForm()
    context = {
        'form': form
    }
    return render(request, 'contacts/contact_form.html', context)


def contact_success(request):
    return render(request, 'contacts/contact_success.html')
