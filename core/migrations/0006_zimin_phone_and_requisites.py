from django.db import migrations, models


def apply_zimin_contact(apps, schema_editor):
    SiteSettings = apps.get_model('core', 'SiteSettings')
    for row in SiteSettings.objects.all():
        row.main_phone = '+7 (983) 113-82-55'
        row.company_legal_name = 'ИП Зимин Евгений Николаевич'
        row.company_inn = ''
        row.company_ogrn = ''
        row.company_rs = ''
        row.company_bank = ''
        row.save(
            update_fields=[
                'main_phone',
                'company_legal_name',
                'company_inn',
                'company_ogrn',
                'company_rs',
                'company_bank',
            ]
        )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_sitesettings_email_and_meta_defaults'),
    ]

    operations = [
        migrations.RunPython(apply_zimin_contact, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='sitesettings',
            name='main_phone',
            field=models.CharField(default='+7 (983) 113-82-55', max_length=30),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='company_legal_name',
            field=models.CharField(
                default='ИП Зимин Евгений Николаевич',
                max_length=200,
                verbose_name='ИП / наименование организации',
            ),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='company_inn',
            field=models.CharField(blank=True, default='', max_length=20, verbose_name='ИНН'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='company_ogrn',
            field=models.CharField(blank=True, default='', max_length=20, verbose_name='ОГРН / ОГРНИП'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='company_rs',
            field=models.CharField(blank=True, default='', max_length=34, verbose_name='Расчётный счёт'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='company_bank',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Банк'),
        ),
    ]
