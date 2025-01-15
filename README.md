# SmartFridge-backend

## Структура бд

https://cloud.predprof.olimpiada.ru/index.php/s/Rgcom3K2BHRMqDJ

### Типы продуктов
* `id`: айди
* `name`: название

Например, "хлеб", "м(c)асло"

### Виды продуктов
* `id`: айди вида продуктов
* `название`: название продукта (например, "батон нарезной")
* `id типа`: айди типа из таблицы типы продуктов
* `масса`: (в си)
* `объём`: (в си)
* `пищевая ценность`: (в ккал?)
* `тип измерения`: не совсем шарю зачем но ладно, (например: картофель - вес, йогурт - штуки)

### Продукты
* `id`: айди конкретного продукта в холодильнике
* `id вида`: айди вида продукта из таблицы виды продуктов
* `дата производства`
* `срок годности` (или лучше дата истечения хз)