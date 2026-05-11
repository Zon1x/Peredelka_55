from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['author_name', 'author_position', 'service_type', 'text', 'rating']
        labels = {
            'service_type': 'Тип работ / услуги',
        }
        widgets = {
            'author_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'author_position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваша должность (необязательно)'}),
            'service_type': forms.Select(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Ваш отзыв'}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
        }
