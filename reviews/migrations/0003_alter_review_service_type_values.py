from django.db import migrations, models


def remap_service_types(apps, schema_editor):
    Review = apps.get_model('reviews', 'Review')
    mapping = {
        'other': 'frame_repair',
        'evacuator': 'euro_van',
        'kmu': 'frame_repair',
        'vacuum': 'frame_repair',
        'gbo': 'frame_repair',
        'complex': 'euro_van',
    }
    for review in Review.objects.all():
        new_val = mapping.get(review.service_type)
        if new_val:
            review.service_type = new_val
            review.save(update_fields=['service_type'])


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_review_service_type'),
    ]

    operations = [
        migrations.RunPython(remap_service_types, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='review',
            name='service_type',
            field=models.CharField(
                choices=[
                    ('frame_extension', 'Удлинение рамы'),
                    ('euro_van', 'Еврофургон'),
                    ('inspection', 'Техосмотр'),
                    ('frame_repair', 'Ремонт рамы'),
                ],
                default='frame_repair',
                max_length=32,
                verbose_name='Тип услуги',
            ),
        ),
    ]
