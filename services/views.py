from django.http import Http404
from django.shortcuts import render, get_object_or_404

from .constants import FOUR_CORE_SERVICE_NAMES, is_core_service, topic_image_url_for_service_name
from .models import Service


def service_list(request):
    services = list(
        Service.objects.filter(is_active=True, name__in=FOUR_CORE_SERVICE_NAMES).select_related('category')
    )
    for service in services:
        service.topic_image_url = topic_image_url_for_service_name(service.name)

    context = {
        'services': services,
        'fixed_service_names': list(FOUR_CORE_SERVICE_NAMES),
    }
    return render(request, 'services/service_list.html', context)


def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if not is_core_service(service.name):
        raise Http404()
    return render(request, 'services/service_detail.html', {'service': service})
