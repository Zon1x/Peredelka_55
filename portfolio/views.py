from django.http import Http404
from django.shortcuts import render, get_object_or_404

from .models import PortfolioCategory, PortfolioItem

# Только эти направления в фильтрах «Наши работы»
PORTFOLIO_WORK_SLUGS = ('udlinenie-ramy', 'evrofurgon', 'tehosmotr', 'remont-ramy')


def portfolio_list(request, category_slug=None):
    if category_slug and category_slug not in PORTFOLIO_WORK_SLUGS:
        raise Http404()

    categories = PortfolioCategory.objects.filter(slug__in=PORTFOLIO_WORK_SLUGS).order_by('ordering', 'name')

    portfolio_items = PortfolioItem.objects.select_related('category').all()
    if category_slug:
        selected_category = get_object_or_404(PortfolioCategory, slug=category_slug)
        portfolio_items = portfolio_items.filter(category=selected_category)
    else:
        selected_category = None

    portfolio_cards = list(portfolio_items)
    fallback_cards = [
        {
            'title': 'Удлинение рамы ГАЗель',
            'category_name': 'Удлинение рамы',
            'year': '2026',
            'price_display': 'от 100 000 руб.',
            'image_url': '/static/img/udlinenie_ramy.svg',
        },
        {
            'title': 'Еврофургон 6.2 м',
            'category_name': 'Еврофургон',
            'year': '2026',
            'price_display': 'от 200 000 руб.',
            'image_url': '/static/img/evrofurgon.svg',
        },
        {
            'title': 'Техосмотр и подготовка',
            'category_name': 'Техосмотр',
            'year': '2026',
            'price_display': 'от 5 000 руб.',
            'image_url': '/static/img/tehosmotr.svg',
        },
        {
            'title': 'Ремонт и усиление рамы',
            'category_name': 'Ремонт рамы',
            'year': '2026',
            'price_display': 'от 20 000 руб.',
            'image_url': '/static/img/remont_ramy.svg',
        },
        {
            'title': 'Комплекс: рама и фургон',
            'category_name': 'Еврофургон',
            'year': '2025',
            'price_display': 'индивидуальный расчёт',
            'image_url': '/static/img/proizvodstvennaya_zona.svg',
        },
        {
            'title': 'Восстановление после нагрузки',
            'category_name': 'Ремонт рамы',
            'year': '2025',
            'price_display': 'от 20 000 руб.',
            'image_url': '/static/img/remont_ramy.svg',
        },
    ]
    while len(portfolio_cards) < 6:
        portfolio_cards.append(fallback_cards[len(portfolio_cards)])

    context = {
        'categories': categories,
        'portfolio_items': portfolio_items,
        'portfolio_cards': portfolio_cards,
        'selected_category': selected_category,
    }
    return render(request, 'portfolio/portfolio_list.html', context)


def portfolio_detail(request, pk):
    portfolio_item = get_object_or_404(PortfolioItem, pk=pk)
    return render(request, 'portfolio/portfolio_detail.html', {'portfolio_item': portfolio_item})
