from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Promotion
from .forms import PromotionReviewLinkForm


def promotion_list(request):
    promotions = Promotion.objects.filter(is_active=True)
    return render(request, 'promotions/promotion_list.html', {'promotions': promotions})


def promotion_detail(request, slug):
    promotion = get_object_or_404(Promotion, slug=slug, is_active=True)
    form = PromotionReviewLinkForm()
    if request.method == 'POST':
        form = PromotionReviewLinkForm(request.POST)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.promotion = promotion
            sub.save()
            messages.success(request, 'Спасибо! Мы проверим ссылку и свяжемся с вами по условиям акции.')
            return redirect('promotions:promotion_detail', slug=promotion.slug)
    return render(
        request,
        'promotions/promotion_detail.html',
        {'promotion': promotion, 'form': form},
    )
