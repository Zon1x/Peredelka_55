from django.db import migrations


def ensure_four_portfolio_categories(apps, schema_editor):
    PortfolioCategory = apps.get_model('portfolio', 'PortfolioCategory')
    rows = [
        ('Удлинение рамы', 'udlinenie-ramy', 0),
        ('Еврофургон', 'evrofurgon', 1),
        ('Техосмотр', 'tehosmotr', 2),
        ('Ремонт рамы', 'remont-ramy', 3),
    ]
    for name, slug, ordering in rows:
        obj, created = PortfolioCategory.objects.get_or_create(
            slug=slug,
            defaults={'name': name, 'ordering': ordering, 'description': ''},
        )
        if not created and obj.name != name:
            obj.name = name
            obj.ordering = ordering
            obj.save(update_fields=['name', 'ordering'])


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0005_alter_portfolioitem_images_optional'),
    ]

    operations = [
        migrations.RunPython(ensure_four_portfolio_categories, migrations.RunPython.noop),
    ]
