# Generated manually for Omsk address, requisites, data refresh

from django.db import migrations, models


def forwards_address_omsk(apps, schema_editor):
    SiteSettings = apps.get_model('core', 'SiteSettings')
    for s in SiteSettings.objects.all():
        a = s.address or ''
        if 'Нижний Новгород' in a or 'Фучика' in a:
            s.address = 'г. Омск, ул. Молодежная, д. 10'
            s.save(update_fields=['address'])


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_sitesettings_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='company_bank',
            field=models.CharField(default='ПАО Сбербанк, г. Омск', max_length=255, verbose_name='Банк'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='company_inn',
            field=models.CharField(default='550812345678', max_length=20, verbose_name='ИНН'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='company_legal_name',
            field=models.CharField(
                default='ИП Петров Сергей Александрович',
                max_length=200,
                verbose_name='ИП / наименование организации',
            ),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='company_ogrn',
            field=models.CharField(default='304550812345678', max_length=20, verbose_name='ОГРН / ОГРНИП'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='company_rs',
            field=models.CharField(
                default='40802810955000001234',
                max_length=34,
                verbose_name='Расчётный счёт',
            ),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='address',
            field=models.CharField(default='г. Омск, ул. Молодежная, д. 10', max_length=255),
        ),
        migrations.RunPython(forwards_address_omsk, migrations.RunPython.noop),
    ]
