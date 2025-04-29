# lib_shop_api

`lib_shop_api` это библиотека Python предоставляет api для получения информации о товарах с сайта

## Установка из PyPI

```bash
pip install lib_shop_api
```

## Использование репозитория GitHub

```bash
git clone https://github.com/YuranIgnatenko/lib_shop_api.git
cd lib_shop_api
pip install .
```

## Пример использования

```python
# импорт парсера
from lib_shop_api import Parser
# имрорт категорий товаров для поиска
from lib_shop_api.constants import K_NOTEBOOK, K_MONITOR, K_DVD

# создание парсера
parser = Parser()

# получение количества всех страниц
count_pages = parser.get_count_pages(K_NOTEBOOK)

# получение количества всего товара из категории
count_products = parser.get_count_products(K_MONITOR)

# получение списка товаров в виде объектов класса models.Product
number_page = 1
products = parser.get_products(K_DVD, number_page)

# получить поля продукта
product = products[0]

print(str(product))
print(product.title)
print(product.image)
print(product.price)
print(product.description)

# получиени из итератора
#с указанием максимально возможного кол-ва
#продуктов на выходе
max_wait_out_product = 5
for product in parser.get_products_iterator(K_DVD, max_wait_out_product)
	print(product.title)

```

> using sources from site:
> `https://skypka.com/`
