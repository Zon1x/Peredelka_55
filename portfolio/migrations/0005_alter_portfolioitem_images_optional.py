from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0004_portfolioitem_chassis_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolioitem',
            name='after_image',
            field=models.ImageField(blank=True, null=True, upload_to='portfolio/after/', verbose_name='Фото после'),
        ),
        migrations.AlterField(
            model_name='portfolioitem',
            name='before_image',
            field=models.ImageField(blank=True, null=True, upload_to='portfolio/before/', verbose_name='Фото до'),
        ),
    ]
