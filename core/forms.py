from django import forms

from services.constants import FOUR_CORE_SERVICE_NAMES, price_from_for_service_name


class VehicleConstructorForm(forms.Form):
    """Подбор параметров конфигурации (аналог калькулятора на специализированных сайтах по переоборудованию)."""

    chassis = forms.ChoiceField(
        label='Класс шасси',
        choices=[
            ('light', 'Лёгкий коммерческий (ГАЗель и аналоги)'),
            ('medium', 'Среднетоннаж (до 12 т)'),
            ('heavy', 'Тяжёлое шасси / сложная геометрия рамы'),
        ],
        initial='light',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    service = forms.ChoiceField(
        label='Тип работ',
        choices=[(n, n) for n in FOUR_CORE_SERVICE_NAMES],
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    euro_body_length = forms.ChoiceField(
        label='Длина кузова (только для еврофургона)',
        required=False,
        choices=[
            ('', '— не применяется / стандарт —'),
            ('4', 'до 4 м'),
            ('5', '4–5 м'),
            ('6', '5–6 м'),
            ('6plus', 'свыше 6 м'),
        ],
        initial='',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    workload = forms.ChoiceField(
        label='Объём и приоритет сроков',
        choices=[
            ('standard', 'Стандартный график'),
            ('extended', 'Расширенный объём работ'),
            ('urgent', 'Срочный приоритет в производстве'),
        ],
        initial='standard',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('service') != 'Еврофургон':
            cleaned['euro_body_length'] = ''
        return cleaned

    @classmethod
    def choice_label(cls, field_name: str, value: str) -> str:
        field = cls.base_fields[field_name]
        return dict(field.choices).get(value, value)

    @staticmethod
    def estimate_price(cleaned_data: dict) -> tuple[int, int, float]:
        """Возвращает (min_rub, max_rub, mid_rub) для отображения."""
        service_name = cleaned_data['service']
        chassis = cleaned_data['chassis']
        workload = cleaned_data.get('workload') or 'standard'
        euro_len = cleaned_data.get('euro_body_length') or ''

        chassis_mult = {'light': 1.0, 'medium': 1.12, 'heavy': 1.28}
        workload_mult = {'standard': 1.0, 'extended': 1.15, 'urgent': 1.28}
        euro_addon = {'': 0, '4': 0, '5': 12000, '6': 28000, '6plus': 45000}

        base = float(price_from_for_service_name(service_name))
        if base <= 0:
            base = 5000.0

        total = base * chassis_mult.get(chassis, 1.0) * workload_mult.get(workload, 1.0)
        if service_name == 'Еврофургон':
            total += float(euro_addon.get(euro_len, 0))

        minimum = int(total * 0.88)
        maximum = int(total * 1.12)
        mid = (minimum + maximum) / 2
        return minimum, maximum, mid
