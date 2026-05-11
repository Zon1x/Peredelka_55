from django import forms
from .models import PromotionReviewSubmission


class PromotionReviewLinkForm(forms.ModelForm):
    class Meta:
        model = PromotionReviewSubmission
        fields = ['name', 'phone', 'review_url', 'comment']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Как к вам обращаться'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Телефон (необязательно)'}),
            'review_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Комментарий (необязательно)'}),
        }
