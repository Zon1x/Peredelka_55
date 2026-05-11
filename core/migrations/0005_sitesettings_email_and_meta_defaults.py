from django.db import migrations, models


def set_main_email(apps, schema_editor):
    SiteSettings = apps.get_model('core', 'SiteSettings')
    legacy = ('avtorekord-nn@mail.ru', 'info@peredelka55-omsk.ru')
    for row in SiteSettings.objects.all():
        em = (row.main_email or '').strip().lower()
        if em in legacy:
            row.main_email = 'jeka_22.09.83@mail.ru'
            row.save(update_fields=['main_email'])


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_sitesettings_company_requisites_and_address'),
    ]

    operations = [
        migrations.RunPython(set_main_email, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='sitesettings',
            name='main_email',
            field=models.EmailField(default='jeka_22.09.83@mail.ru', max_length=254),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='default_meta_description',
            field=models.TextField(
                default='Омск: удлинение рамы, изготовление и монтаж еврофургона, подготовка к техосмотру, ремонт и восстановление рамы грузового транспорта. Ориентировочные цены и сроки — после осмотра.',
            ),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='keywords',
            field=models.CharField(
                default='удлинение рамы, еврофургон, техосмотр, ремонт рамы, Омск, грузовой транспорт',
                max_length=255,
            ),
        ),
    ]
