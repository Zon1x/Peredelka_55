"""Единый перечень услуг сайта, цены «от» и пути к статическим изображениям (понятные имена файлов)."""

FOUR_CORE_SERVICE_NAMES = (
    'Удлинение рамы',
    'Еврофургон',
    'Техосмотр',
    'Ремонт рамы',
)

# Ключ — фрагмент названия услуги в нижнем регистре; значение — базовая цена «от»
SERVICE_PRICE_FROM_BY_KEYWORD = {
    'техосмотр': 5000,
    'ремонт рамы': 20000,
    'удлинение рамы': 100000,
    'еврофургон': 200000,
}

# Имена файлов в static/img/ (латиница для совместимости)
SERVICE_IMAGE_STATIC = {
    'удлинение рамы': '/static/img/udlinenie_ramy.svg',
    'еврофургон': '/static/img/evrofurgon.svg',
    'техосмотр': '/static/img/tehosmotr.svg',
    'ремонт рамы': '/static/img/remont_ramy.svg',
}


def topic_image_url_for_service_name(name: str) -> str:
    lname = (name or '').lower()
    for key, url in SERVICE_IMAGE_STATIC.items():
        if key in lname:
            return url
    return '/static/img/zaglushka_uslugi.svg'


def price_from_for_service_name(name: str) -> int:
    n = (name or '').lower()
    for key, amount in SERVICE_PRICE_FROM_BY_KEYWORD.items():
        if key in n:
            return amount
    return 0


def is_core_service(name: str) -> bool:
    return (name or '').strip() in FOUR_CORE_SERVICE_NAMES
