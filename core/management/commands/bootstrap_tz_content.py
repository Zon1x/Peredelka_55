"""
Первичное наполнение по ТЗ (если таблицы пустые): настройки, статистика,
четыре услуги (удлинение рамы, еврофургон, техосмотр, ремонт рамы), акция,
категории портфолио. Опционально — демо-отзывы.
"""
from datetime import date, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand

from core.models import SiteSettings, Statistic
from promotions.models import Promotion
from portfolio.models import PortfolioCategory
from reviews.models import Review
from services.models import Service, ServiceCategory


TZ_ADDRESS = 'г. Омск, ул. Рельсовая, д. 25'
TZ_PHONE = '+7 (983) 113-82-55'
TZ_EMAIL = 'jeka_22.09.83@mail.ru'

SERVICE_GROUPS = [
    {
        'name': 'Удлинение рамы',
        'icon': 'fa-ruler-horizontal',
        'description': (
            'Проектирование усиления и удлинения рамы под заданную колёсную базу и тип надстройки. '
            'Замеры на вашем шасси, расчёт узлов, сварка, контроль геометрии и антикоррозийная обработка зон шва. '
            'Работаем с полуприцепами, среднетоннажными и лёгкими коммерческими шасси. '
            'Перед началом согласуем объём: только удлинение лонжеронов, установка вставок, перенос опор и т.д.'
        ),
        'service_name': 'Удлинение рамы',
        'service_desc': (
            '<p>Удлинение рамы выполняется по техническому заданию и результатам осмотра: фиксируем исходную длину, '
            'требуемую базу, тип будущего фургона или борта, допустимые нагрузки на ось.</p>'
            '<p>На производстве разрабатывается схема усиления (вставки, накладки, распределение швов), '
            'подбирается электродная проволока и режимы сварки, выполняется контроль углов и плоскостей. '
            'После сборки — грунтовка и окраска открытых металлоконструкций, рекомендации по обкатке и ТО.</p>'
            '<p><strong>Ориентировочная стоимость — от 100&nbsp;000 руб.</strong> Итог зависит от сложности '
            'конструкции шасси, объёма усиления и срочности.</p>'
        ),
        'price_from': Decimal('100000.00'),
    },
    {
        'name': 'Еврофургон',
        'icon': 'fa-truck',
        'description': (
            'Изготовление кузова-фургона по типовым и индивидуальным модулям: длина кузова, высота ворот, '
            'тип пола (фанера, металл, решётка), вентиляция, запираемые люки, внутренняя обшивка. '
            'Монтаж на подготовленное шасси с учётом распределения массы и крепления к раме.'
        ),
        'service_name': 'Еврофургон',
        'service_desc': (
            '<p>Еврофургон изготавливается из сэндвич-панелей или металлокаркаса с утеплением — вариант '
            'согласуем на этапе договора. Продумываем расположение дверей, крепления ремней, карманов под инструмент.</p>'
            '<p>После монтажа проверяем герметичность, работу замков и петель, при необходимости устанавливаем '
            'внутреннее освещение и розетки по согласованию.</p>'
            '<p><strong>Ориентировочная стоимость — от 200&nbsp;000 руб.</strong> На цену влияют габариты, '
            'комплектация и сопутствующие работы по раме.</p>'
        ),
        'price_from': Decimal('200000.00'),
    },
    {
        'name': 'Техосмотр',
        'icon': 'fa-clipboard-check',
        'description': (
            'Подготовка грузового автомобиля к прохождению техосмотра после переоборудования или ремонта: '
            'проверка светотехники, тормозов, рулевого, видимости номеров, утечек рабочих жидкостей. '
            'Консультируем по пакету документов и срокам записи.'
        ),
        'service_name': 'Техосмотр',
        'service_desc': (
            '<p>Мы не заменяем официальную диагностическую линию, но помогаем устранить типовые замечания до визита '
            'на пункт ТО: регулировка фар, крепление брызговиков, маркировка, доступ к VIN.</p>'
            '<p>При необходимости составляем перечень выполненных работ для предъявления инспектору.</p>'
            '<p><strong>Ориентировочная стоимость подготовки — от 5&nbsp;000 руб.</strong> Финальная сумма '
            'зависит от объёма доработок и состояния техники.</p>'
        ),
        'price_from': Decimal('5000.00'),
    },
    {
        'name': 'Ремонт рамы',
        'icon': 'fa-tools',
        'description': (
            'Диагностика трещин, коррозии и деформаций рамы. Локальный ремонт лонжеронов, замена участков, '
            'варка усилителей, восстановление креплений рессор и балок. После ремонта даём рекомендации по эксплуатации '
            'и повторному осмотру через оговорённый интервал пробега.'
        ),
        'service_name': 'Ремонт рамы',
        'service_desc': (
            '<p>Начинаем с визуального осмотра и, при необходимости, замеров прогиба. Определяем, достаточно ли '
            'локальной вырубки дефектного металла с последующей наваркой усилителя или требуется смена целого участка.</p>'
            '<p>Используем проверенные технологии сварки, контролируем качество швов, обрабатываем зоны '
            'антикоррозионным составом.</p>'
            '<p><strong>Ориентировочная стоимость — от 20&nbsp;000 руб.</strong> Сложный случай (множественные '
            'трещины, критическая коррозия) оценивается отдельно.</p>'
        ),
        'price_from': Decimal('20000.00'),
    },
]

PORTFOLIO_CATEGORIES = [
    ('Удлинение рамы', 'udlinenie-ramy'),
    ('Еврофургон', 'evrofurgon'),
    ('Техосмотр', 'tehosmotr'),
    ('Ремонт рамы', 'remont-ramy'),
]

DEMO_REVIEWS = [
    ('Алексей', 'frame_extension', 5, 'Удлинили раму на ГАЗели под еврофургон 6 м. Сроки выдержали, по документам всё чисто, скрытых доплат не было.'),
    ('Марина', 'euro_van', 5, 'Заказали новый еврофургон вместе с доработкой рамы. Персонал вежливый, цена адекватная, всё объяснили по этапам.'),
    ('Игорь', 'inspection', 5, 'Помогли подготовить машину к ТО после ремонта рамы — прошли с первого раза, спасибо за чек-лист.'),
    ('Сергей', 'frame_repair', 5, 'Рама треснула у крепления рессоры — усилили и заварили аккуратно. Через месяц осмотр — без замечаний.'),
    ('Дмитрий', 'euro_van', 4, 'Еврофургон на заказ, чуть задержали поставку фурнитуры, но предупредили заранее. Качеством доволен.'),
]


class Command(BaseCommand):
    help = 'Создаёт стартовый контент по ТЗ (настройки, услуги, акции, категории портфолио), если их ещё нет.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--demo-reviews',
            action='store_true',
            help='Добавить демонстрационные опубликованные отзывы (если опубликованных меньше 5).',
        )

    def handle(self, *args, **options):
        self._ensure_site_settings()
        self._ensure_statistic()
        self._ensure_service_categories()
        self._ensure_portfolio_categories()
        self._ensure_promotions()
        if options['demo_reviews']:
            self._ensure_demo_reviews()
        self.stdout.write(self.style.SUCCESS('Готово. Обновите страницу в браузере (Ctrl+F5).'))

    def _ensure_site_settings(self):
        if SiteSettings.objects.exists():
            self.stdout.write('Настройки сайта уже есть — пропуск.')
            return
        SiteSettings.objects.create(
            site_name='Peredelka55',
            company_name='Peredelka55',
            main_phone=TZ_PHONE,
            main_email=TZ_EMAIL,
            company_legal_name='ИП Зимин Евгений Николаевич',
            address=TZ_ADDRESS,
            working_hours='Пн–Пт: 9:00–18:00',
            default_meta_title='Переоборудование коммерческого транспорта | Peredelka55',
            default_meta_description=(
                'Омск: удлинение рамы, еврофургон, подготовка к техосмотру, ремонт рамы. '
                'Ориентировочные цены — после осмотра и согласования объёма работ.'
            ),
            keywords='удлинение рамы, еврофургон, техосмотр, ремонт рамы, Омск, грузовой транспорт',
        )
        self.stdout.write(self.style.SUCCESS('Созданы настройки сайта (адрес и контакты по ТЗ).'))

    def _ensure_statistic(self):
        if Statistic.objects.exists():
            self.stdout.write('Статистика уже есть — пропуск.')
            return
        Statistic.objects.create(
            projects_completed=7000,
            years_of_experience=15,
            satisfied_clients_percentage=98,
            specialists_count=25,
        )
        self.stdout.write(self.style.SUCCESS('Создана статистика (7000+ проектов, 15+ лет).'))

    def _ensure_service_categories(self):
        if ServiceCategory.objects.exists():
            self.stdout.write('Категории услуг уже есть — пропуск.')
            return
        for i, row in enumerate(SERVICE_GROUPS):
            cat = ServiceCategory.objects.create(
                name=row['name'],
                description=row['description'],
                icon=row['icon'],
                ordering=i,
            )
            Service.objects.create(
                category=cat,
                name=row['service_name'],
                description=row['service_desc'],
                price_from=row['price_from'],
                terms='Сроки: от нескольких дней для подготовки к ТО до нескольких недель для комплекса рама+фургон — уточняйте у менеджера.',
                guarantee='Гарантия на выполненные сварочные и монтажные работы — по договору; условия фиксируются в акте приёмки.',
                specialist_visit=True,
                work_process=(
                    '1) Заявка и консультация по телефону или через форму на сайте.\n'
                    '2) Осмотр техники, согласование объёма и сметы.\n'
                    '3) Выполнение работ на производстве с промежуточными согласованиями.\n'
                    '4) Приёмка, рекомендации по эксплуатации и дальнейшему обслуживанию.'
                ),
                is_active=True,
            )
        self.stdout.write(self.style.SUCCESS(f'Создано {len(SERVICE_GROUPS)} категорий и карточек услуг.'))

    def _ensure_portfolio_categories(self):
        if PortfolioCategory.objects.exists():
            self.stdout.write('Категории портфолио уже есть — пропуск.')
            return
        for i, (name, slug) in enumerate(PORTFOLIO_CATEGORIES):
            PortfolioCategory.objects.create(
                name=name,
                slug=slug,
                description='',
                ordering=i,
            )
        self.stdout.write(self.style.SUCCESS('Созданы категории портфолио для фильтров «Наши работы».'))

    def _ensure_promotions(self):
        if Promotion.objects.exists():
            self.stdout.write('Акции уже есть — пропуск.')
            return
        end = date.today() + timedelta(days=90)
        Promotion.objects.create(
            title='Бонус за отзыв на Яндекс.Картах или видео',
            slug='bonus-za-otzyv',
            teaser='Разместите отзыв о нашей работе — получите бонус на следующий заказ.',
            bonus_summary='до 2000 ₽',
            description=(
                'Участвуйте в программе лояльности: оставьте честный отзыв на Яндекс.Картах, '
                'запишите короткое видео на YouTube или ВК и отправьте ссылку через форму на странице акции. '
                'Размер бонуса и условия согласуются с менеджером после проверки публикации.'
            ),
            conditions=(
                'Отзыв должен быть публичным, содержать описание выполненных работ и не противоречить правилам площадки. '
                'Один бонус на один завершённый заказ, если не оговорено иное.'
            ),
            how_to_get='Заполните форму «Отправить ссылку на отзыв» на странице акции. После модерации с вами свяжется менеджер.',
            start_date=date.today(),
            end_date=end,
            is_active=True,
            ordering=0,
        )
        Promotion.objects.create(
            title='Розыгрыш призов при заказе еврофургона',
            slug='rozygrysh-evrofuragon',
            teaser='При заказе комплекта «удлинение + еврофургон» — участие в розыгрыше призов (наборы инструмента, брендированная продукция и др.).',
            bonus_summary='Призы по итогам розыгрыша',
            description='Условия и сроки розыгрыша уточняйте у менеджеров — актуальный регламент публикуется на время проведения акции.',
            conditions='Участие для клиентов с оплаченным договором на комплект работ в период проведения акции.',
            how_to_get='После подписания договора менеджер зарегистрирует вас в списке участников.',
            start_date=date.today(),
            end_date=end,
            is_active=True,
            ordering=1,
        )
        self.stdout.write(self.style.SUCCESS('Созданы 2 демонстрационные акции.'))

    def _ensure_demo_reviews(self):
        added = 0
        for name, stype, rating, text in DEMO_REVIEWS:
            if Review.objects.filter(is_published=True).count() >= 5:
                break
            if Review.objects.filter(is_published=True, author_name=name, text=text).exists():
                continue
            Review.objects.create(
                author_name=name,
                author_position='Клиент',
                service_type=stype,
                text=text,
                rating=rating,
                is_published=True,
            )
            added += 1
        if added:
            self.stdout.write(self.style.SUCCESS(f'Добавлено демо-отзывов: {added}.'))
        else:
            self.stdout.write('Демо-отзывы не нужны (уже есть 5+ или дубликаты).')
