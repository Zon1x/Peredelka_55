from django.db.models import Prefetch
from django.shortcuts import render, redirect

from contacts.forms import QuickContactForm
from contacts.views import notify_new_contact_request
from portfolio.models import PortfolioItem
from promotions.models import Promotion
from reviews.models import Review
from services.constants import FOUR_CORE_SERVICE_NAMES
from services.models import Service, ServiceCategory

from .forms import VehicleConstructorForm
from .models import Statistic


def index(request):
    constructor_form = VehicleConstructorForm()
    quick_form = QuickContactForm()
    estimated_cost = None
    estimated_cost_min = None
    estimated_cost_max = None
    selected_service = None
    constructor_summary = None

    if request.method == 'POST':
        submit = request.POST.get('submit')
        if submit == 'quick':
            quick_form = QuickContactForm(request.POST)
            if quick_form.is_valid():
                contact = quick_form.save()
                notify_new_contact_request(contact, request=request)
                return redirect('contact_success')
        elif submit == 'constructor':
            constructor_form = VehicleConstructorForm(request.POST)
            if constructor_form.is_valid():
                cd = constructor_form.cleaned_data
                estimated_cost_min, estimated_cost_max, estimated_cost = VehicleConstructorForm.estimate_price(cd)
                service_name = cd['service']
                selected_service = (
                    Service.objects.filter(name=service_name, is_active=True)
                    .order_by('pk')
                    .first()
                )
                euro_raw = cd.get('euro_body_length') or ''
                constructor_summary = {
                    'chassis': VehicleConstructorForm.choice_label('chassis', cd['chassis']),
                    'service': service_name,
                    'workload': VehicleConstructorForm.choice_label('workload', cd['workload']),
                    'euro_body_length': euro_raw or None,
                    'euro_body_label': VehicleConstructorForm.choice_label('euro_body_length', euro_raw)
                    if euro_raw
                    else None,
                }

    try:
        statistics = Statistic.objects.get()
    except Statistic.DoesNotExist:
        statistics = None

    featured_portfolio = (
        PortfolioItem.objects.select_related('category')
        .order_by('-completion_date', '-pk')[:6]
    )
    placeholder_offers = [
        ('Удлинение рамы под еврофургон', 'от 100 000 ₽, точная сумма после замеров', '/static/img/udlinenie_ramy.svg'),
        ('Еврофургон под ключ', 'от 200 000 ₽, зависит от длины и комплектации', '/static/img/evrofurgon.svg'),
        ('Подготовка к техосмотру', 'от 5 000 ₽, по объёму доработок', '/static/img/tehosmotr.svg'),
        ('Ремонт и усиление рамы', 'от 20 000 ₽, после диагностики', '/static/img/remont_ramy.svg'),
        ('Комплект: рама + фургон', 'индивидуальный расчёт', '/static/img/proizvodstvennaya_zona.svg'),
        ('Срочный ремонт несущей', 'по согласованию', '/static/img/remont_ramy.svg'),
    ]
    ready_solutions = list(featured_portfolio)
    for idx in range(len(ready_solutions), 6):
        title, price_display, image_url = placeholder_offers[idx % len(placeholder_offers)]
        ready_solutions.append({
            'title': title,
            'price_display': price_display,
            'image_url': image_url,
            'url': '/portfolio/',
        })
    featured_reviews = list(
        Review.objects.filter(is_published=True).order_by('-created_at')[:7]
    )
    active_promotions = Promotion.objects.filter(is_active=True).order_by('ordering', '-start_date')[:4]
    service_categories = (
        ServiceCategory.objects.prefetch_related(
            Prefetch(
                'services',
                queryset=Service.objects.filter(
                    is_active=True, name__in=FOUR_CORE_SERVICE_NAMES
                ).order_by('name'),
            )
        )
        .filter(services__name__in=FOUR_CORE_SERVICE_NAMES)
        .distinct()
        .order_by('ordering', 'name')[:8]
    )

    context = {
        'constructor_form': constructor_form,
        'quick_form': quick_form,
        'estimated_cost': estimated_cost,
        'estimated_cost_min': estimated_cost_min,
        'estimated_cost_max': estimated_cost_max,
        'selected_service': selected_service,
        'constructor_summary': constructor_summary,
        'statistics': statistics,
        'featured_portfolio': featured_portfolio,
        'ready_solutions': ready_solutions,
        'featured_reviews': featured_reviews,
        'active_promotions': active_promotions,
        'service_categories': service_categories,
    }
    return render(request, 'index.html', context)


def about(request):
    return render(request, 'about.html')


def page_not_found_view(request, exception):
    return render(request, '404.html', {}, status=404)


def server_error_view(request):
    return render(request, '500.html', {}, status=500)
