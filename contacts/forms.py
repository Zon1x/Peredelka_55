from django import forms
import re
from .models import ContactRequest
from services.constants import FOUR_CORE_SERVICE_NAMES
from services.models import Service


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['name', 'vehicle_type', 'phone', 'email', 'service', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'vehicle_type': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Тип авто / интересующая услуга (необязательно)'}
            ),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш телефон', 'type': 'tel', 'inputmode': 'tel', 'pattern': r'[\d\+\-\(\)\s]+'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ваш Email (необязательно)'}),
            'service': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Ваше сообщение (необязательно)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].queryset = Service.objects.filter(
            is_active=True, name__in=FOUR_CORE_SERVICE_NAMES
        ).order_by('name')
        self.fields['service'].empty_label = 'Выберите услугу (необязательно)'
        self.fields['name'].required = True
        self.fields['phone'].required = False

    def clean_phone(self):
        phone = (self.cleaned_data.get('phone') or '').strip()
        if not phone:
            return phone
        cleaned = re.sub(r'[^\d+]', '', phone)
        if not re.fullmatch(r'\+?\d{10,15}', cleaned):
            raise forms.ValidationError('Введите корректный номер телефона.')
        return cleaned


class QuickContactForm(forms.ModelForm):
    """Быстрая заявка с главной: тип авто / услуги, телефон, комментарий."""

    class Meta:
        model = ContactRequest
        fields = ['vehicle_type', 'phone', 'message']
        labels = {
            'vehicle_type': 'Тип автомобиля или услуга',
            'phone': 'Телефон',
            'message': 'Комментарий',
        }
        widgets = {
            'vehicle_type': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Например: ГАЗель Next, удлинение рамы / еврофургон 6 м / техосмотр / ремонт рамы',
                    'autocomplete': 'off',
                }
            ),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Телефон для связи', 'type': 'tel', 'inputmode': 'tel', 'pattern': r'[\d\+\-\(\)\s]+'}),
            'message': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Необязательно: пожелания по срокам, бюджету'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vehicle_type'].required = True
        self.fields['phone'].required = True
        self.fields['message'].required = False

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.name = 'Заявка с главной страницы'
        if commit:
            obj.save()
        return obj

    def clean_phone(self):
        phone = (self.cleaned_data.get('phone') or '').strip()
        cleaned = re.sub(r'[^\d+]', '', phone)
        if not re.fullmatch(r'\+?\d{10,15}', cleaned):
            raise forms.ValidationError('Введите корректный номер телефона.')
        return cleaned
