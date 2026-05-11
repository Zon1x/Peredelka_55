from decimal import Decimal

from django.db import migrations


def ensure_services(apps, schema_editor):
    ServiceCategory = apps.get_model('services', 'ServiceCategory')
    Service = apps.get_model('services', 'Service')

    rows = [
        {
            'name': 'Удлинение рамы',
            'icon': 'fa-ruler-horizontal',
            'price_from': Decimal('100000'),
            'description': '<p>Проект усиления и удлинения рамы под согласованную базу. Ориентир «от» 100&nbsp;000 руб.; итог после осмотра.</p>',
        },
        {
            'name': 'Еврофургон',
            'icon': 'fa-truck',
            'price_from': Decimal('200000'),
            'description': '<p>Изготовление и монтаж кузова по параметрам заказчика. Ориентир «от» 200&nbsp;000 руб.</p>',
        },
        {
            'name': 'Техосмотр',
            'icon': 'fa-clipboard-check',
            'price_from': Decimal('5000'),
            'description': '<p>Подготовка транспорта к прохождению линии диагностики. Ориентир «от» 5&nbsp;000 руб.</p>',
        },
        {
            'name': 'Ремонт рамы',
            'icon': 'fa-tools',
            'price_from': Decimal('20000'),
            'description': '<p>Диагностика и ремонт несущей, усиление узлов. Ориентир «от» 20&nbsp;000 руб.</p>',
        },
    ]

    for i, row in enumerate(rows):
        cat, _ = ServiceCategory.objects.get_or_create(
            name=row['name'],
            defaults={
                'description': '',
                'icon': row['icon'],
                'ordering': i,
            },
        )
        srv = Service.objects.filter(name=row['name']).order_by('pk').first()
        common = {
            'category': cat,
            'description': row['description'],
            'price_from': row['price_from'],
            'is_active': True,
            'terms': 'Сроки уточняйте после осмотра.',
            'guarantee': 'По отдельным работам условия в договоре.',
            'specialist_visit': True,
            'work_process': 'Осмотр → смета → работы → приёмка.',
        }
        if srv:
            for k, v in common.items():
                setattr(srv, k, v)
            srv.save()
        else:
            Service.objects.create(name=row['name'], **common)


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_service_guarantee_service_specialist_visit_and_more'),
    ]

    operations = [
        migrations.RunPython(ensure_services, migrations.RunPython.noop),
    ]
