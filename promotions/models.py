from django.db import models
from django.urls import reverse


class Promotion(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название акции')
    slug = models.SlugField(max_length=220, unique=True, verbose_name='Слаг')
    teaser = models.TextField(blank=True, verbose_name='Кратко для главной')
    description = models.TextField(verbose_name='Полное описание / условия')
    bonus_summary = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Размер бонуса / приз',
        help_text='Например: до 2000 ₽ за отзыв',
    )
    conditions = models.TextField(blank=True, verbose_name='Условия участия')
    start_date = models.DateField(null=True, blank=True, verbose_name='Дата начала')
    end_date = models.DateField(null=True, blank=True, verbose_name='Дата окончания')
    how_to_get = models.TextField(blank=True, verbose_name='Как получить бонус')
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    ordering = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции и бонусы'
        ordering = ['ordering', '-start_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('promotions:promotion_detail', kwargs={'slug': self.slug})


class PromotionReviewSubmission(models.Model):
    promotion = models.ForeignKey(
        Promotion,
        on_delete=models.CASCADE,
        related_name='review_submissions',
        verbose_name='Акция',
    )
    name = models.CharField(max_length=120, verbose_name='Имя')
    phone = models.CharField(max_length=30, blank=True, verbose_name='Телефон')
    review_url = models.URLField(verbose_name='Ссылка на отзыв')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')
    is_processed = models.BooleanField(default=False, verbose_name='Обработана')

    class Meta:
        verbose_name = 'Заявка на бонус (ссылка на отзыв)'
        verbose_name_plural = 'Заявки на бонус'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.promotion.title}'
