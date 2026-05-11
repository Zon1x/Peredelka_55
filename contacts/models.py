from django.db import models
from services.models import Service

# Create your models here.

class ContactRequest(models.Model):
    name = models.CharField(max_length=100, blank=True, verbose_name="Имя")
    vehicle_type = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Тип авто / услуга",
        help_text="Для быстрой заявки с главной",
    )
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Услуга")
    message = models.TextField(blank=True, verbose_name="Сообщение")
    admin_comment = models.TextField(blank=True, verbose_name="Комментарий администратора")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_processed = models.BooleanField(default=False, verbose_name="Обработана")

    class Meta:
        verbose_name = "Заявка на контакт"
        verbose_name_plural = "Заявки на контакты"
        ordering = ['-created_at']

    def __str__(self):
        return f"Заявка от {self.name} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"
