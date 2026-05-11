from django.db import models

# Create your models here.

class Review(models.Model):
    SERVICE_TYPE_CHOICES = [
        ('frame_extension', 'Удлинение рамы'),
        ('euro_van', 'Еврофургон'),
        ('inspection', 'Техосмотр'),
        ('frame_repair', 'Ремонт рамы'),
    ]
    author_name = models.CharField(max_length=100, verbose_name="Имя автора")
    author_position = models.CharField(max_length=100, blank=True, null=True, verbose_name="Должность автора")
    service_type = models.CharField(
        max_length=32,
        choices=SERVICE_TYPE_CHOICES,
        default='frame_repair',
        verbose_name="Тип услуги",
    )
    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name="Рейтинг")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_published = models.BooleanField(default=False, verbose_name="Опубликован")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']

    def __str__(self):
        return f"Отзыв от {self.author_name} ({self.rating} звезд)"