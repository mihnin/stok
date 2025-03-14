# Система прогнозирования сверхнормативных запасов (СНЗ и КСНЗ)

## Содержание
1. [Общее описание системы](#1-общее-описание-системы)
2. [Методы прогнозирования](#2-методы-прогнозирования)
3. [Подготовка данных](#3-подготовка-данных)
4. [Работа с приложением](#4-работа-с-приложением)
5. [Интерпретация результатов](#5-интерпретация-результатов)
6. [Особые случаи и обработка исключений](#6-особые-случаи-и-обработка-исключений)
7. [Формулы и алгоритмы расчета](#7-формулы-и-алгоритмы-расчета)
8. [Развертывание приложения](#8-развертывание-приложения)

## 1. Общее описание системы

Система прогнозирования сверхнормативных запасов (СНЗ и КСНЗ) предназначена для анализа и прогнозирования уровня складских запасов, которые в будущем могут быть квалифицированы как кандидаты в сверхнормативные (КСНЗ) или сверхнормативные (СНЗ).

Система позволяет определить, когда конкретный материал перейдет в статус КСНЗ или СНЗ, если не будет использован, что дает возможность заблаговременно принять меры по вовлечению материала в производство, предотвращая его переход в категорию неликвидов.

**[Прототип приложения](https://stok01.streamlit.app/)**

### Основные понятия и категории запасов:

| Категория | Описание | Цветовое обозначение |
|-----------|----------|----------------------|
| **Ликвидный запас** | Запас, хранящийся на складе менее определенного периода (обычно до 9 месяцев для Метода 1 и до 10 месяцев для Метода 2). | 🟢 Зеленый (#00b050) |
| **КСНЗ** | Кандидаты в сверхнормативный запас — запас, который находится на грани перехода в сверхнормативный (обычно от 9-10 месяцев до 1 года). | 🟡 Желтый (#ffbf00) |
| **СНЗ** | Сверхнормативный запас — запас, хранящийся на складе дольше допустимого срока (более 1 года до 3 лет). | 🔴 Красный (#ff4c4c) |
| **СНЗ > 3 лет** | Запас, хранящийся на складе более 3 лет, который с высокой вероятностью требует списания. | 🟤 Темно-красный (#c00000) |
| **Требует проверки** | Запасы без указанной даты поступления, которые требуют дополнительной проверки и уточнения данных. | ⚫ Серый (#808080) |

## 2. Методы прогнозирования

### Метод 1: Прогноз на основе данных из отчета ZMML_REP_RD

Этот метод базируется на данных из плоской таблицы отчета ZMML_REP_RD, где "Количество обеспечения" уже учитывает все необходимые факторы. Прогноз показывает переход материалов между категориями запаса с течением времени на основе шкалы старения.

### Метод 2: Прогноз без учета потребности (только фактический запас)

Этот метод основан только на текущем фактическом запасе на складе, без учета потребности и планируемого обеспечения. Он показывает, когда материалы перейдут в категорию КСНЗ или СНЗ, если не будут использованы вообще.

### Шкалы старения запасов

#### Метод 1:
| Интервал | Нижняя граница (дни) | Верхняя граница (дни) | Категория |
|----------|----------------------|----------------------|-----------|
| < 1 месяца | 0 | 30 | Ликвидный |
| 1-3 месяцев | 31 | 91 | Ликвидный |
| 3-6 месяцев | 92 | 183 | Ликвидный |
| 6-9 месяцев | 184 | 274 | Ликвидный |
| 9-12 месяцев | 275 | 365 | КСНЗ |
| 12-18 месяцев | 366 | 548 | СНЗ |
| 18-24 месяца | 549 | 730 | СНЗ |
| 2-3 года | 731 | 1096 | СНЗ |
| 3-4 года | 1097 | 1461 | СНЗ > 3 лет |
| 4-5 лет | 1462 | 1826 | СНЗ > 3 лет |
| > 5 лет | 1827 | 9999 | СНЗ > 3 лет |

#### Метод 2:
| Интервал | Нижняя граница (дни) | Верхняя граница (дни) | Категория |
|----------|----------------------|----------------------|-----------|
| < 1 месяца | 0 | 29 | Ликвидный |
| 1 месяц | 30 | 59 | Ликвидный |
| 2 месяца | 60 | 90 | Ликвидный |
| 3 месяца | 91 | 121 | Ликвидный |
| 4 месяца | 122 | 152 | Ликвидный |
| 5 месяцев | 153 | 182 | Ликвидный |
| 6 месяцев | 183 | 213 | Ликвидный |
| 7 месяцев | 214 | 244 | Ликвидный |
| 8 месяцев | 245 | 273 | Ликвидный |
| 9 месяцев | 274 | 304 | Ликвидный |
| 10 месяцев | 305 | 334 | КСНЗ |
| 11 месяцев | 335 | 364 | КСНЗ |
| 12-18 месяцев | 365 | 547 | СНЗ |
| 18-24 месяца | 548 | 1095 | СНЗ |
| > 3 лет | 1096 | 9999 | СНЗ > 3 лет |
| Без даты в SAP ERP | ≥ 10000 | - | Требует проверки |

## 3. Подготовка данных

### Требования к данным для Метода 1:

| Колонка | Описание | Обязательность |
|---------|----------|---------------|
| БЕ | Бизнес-единица | Обязательно |
| Область планирования | Область планирования | Обязательно |
| Материал | Код материала | Обязательно |
| Количество обеспечения | Текущее количество на складе с учетом обеспечения | Обязательно |
| Дата поступления | Историческая дата поступления или дата поступления на склад | Обязательно |

### Требования к данным для Метода 2:

| Колонка | Описание | Обязательность |
|---------|----------|---------------|
| БЕ | Бизнес-единица | Обязательно |
| Завод | Код завода | Обязательно |
| Склад | Код склада | Обязательно |
| Материал | Код материала | Обязательно |
| Партия | Номер партии | Обязательно |
| СПП элемент | СПП элемент | Обязательно (может быть пустым) |
| Дата поступления на склад | Дата поступления материала на склад | Обязательно |
| Фактический запас | Текущее количество на складе | Обязательно |

## 4. Работа с приложением

Приложение позволяет загружать данные в формате Excel, выбирать метод прогнозирования, настраивать параметры прогноза и просматривать результаты в различных представлениях.

### Основные параметры прогнозирования:

1. **Метод прогнозирования:**
   - Метод 1: На основе данных из отчета ZMML_REP_RD
   - Метод 2: Без учета потребности (только фактический запас)

2. **Источник данных:**
   - Загрузить Excel файл
   - Использовать тестовые данные

3. **Дата окончания прогноза:**
   - Максимальная дата, до которой будет строиться прогноз (до 5 лет от текущей даты)

4. **Шаг прогноза (дни):**
   - Периодичность расчетов прогноза (от 1 до 90 дней)

## 5. Интерпретация результатов

Результаты прогнозирования представлены в нескольких видах:

1. **Сводный график прогноза:**
   Показывает изменение объема запасов в каждой категории на протяжении всего периода прогнозирования. Графики имеют волнообразный характер, отражающий переход запасов из одной категории в другую с течением времени:
   - Падение линии КСНЗ означает, что часть запасов перешла в категорию СНЗ из-за увеличения срока хранения
   - Рост линии КСНЗ показывает переход запасов из категории "Ликвидный" в "Кандидаты в СНЗ"
   - Преобладание СНЗ на долгосрочном прогнозе: При прогнозировании на 2-3 года вперед, большая часть запасов перейдет в категории "СНЗ" и "СНЗ > 3 лет", если не будет использована

2. **Детализация по дате:**
   Позволяет выбрать конкретную дату прогноза и просмотреть распределение запасов по категориям.

3. **Детальная таблица:**
   Содержит подробную информацию по каждому материалу на каждую дату прогноза.

## 6. Особые случаи и обработка исключений

### Работа с партиями с разными датами поступления

Пример:

| БЕ | Завод | Склад | Материал | Партия | Дата поступления | Количество | Категория |
|----|-------|-------|----------|--------|------------------|------------|-----------|
| 0101 | 1111 | 1111 | 222222 | 1111222444 | 27.12.2023 | 30 | КСНЗ |
| 0101 | 1111 | 1111 | 222222 | 1111222444 | 10.01.2024 | 70 | Ликвидный |

В этом примере часть партии поступила в декабре 2023 года (30 единиц), а часть — в январе 2024 года (70 единиц). При прогнозировании система учитывает разные даты поступления и соответствующие категории запаса.

### Материалы без даты поступления

В некоторых случаях в данных может отсутствовать информация о дате поступления материала на склад.

**Обработка:** Материалы без даты поступления помечаются специальной категорией "Требует проверки" и выделяются серым цветом в результатах. Такие материалы требуют дополнительного анализа и уточнения данных.

## 7. Формулы и алгоритмы расчета

### Расчет количества дней хранения

Дни хранения = Дата прогноза - Дата поступления

Этот расчет выполняется для каждого материала на каждую дату прогноза. В результате определяется, сколько дней будет храниться материал к указанной дате прогноза.

### Определение категории запаса (Метод 1)

Если Дни хранения < 275:
Категория = "Ликвидный"
Иначе если Дни хранения < 366:
Категория = "КСНЗ"
Иначе если Дни хранения < 1097:
Категория = "СНЗ"
Иначе:
Категория = "СНЗ > 3 лет"

### Определение категории запаса (Метод 2)

Если Дни хранения < 305:
Категория = "Ликвидный"
Иначе если Дни хранения < 365:
Категория = "КСНЗ"
Иначе если Дни хранения < 1096:
Категория = "СНЗ"
Иначе:
Категория = "СНЗ > 3 лет"

### Алгоритм прогнозирования

Общий алгоритм прогнозирования включает следующие шаги:

1. Определение дат прогноза с заданным шагом от текущей даты до указанной даты окончания прогноза.
2. Для каждой даты прогноза:
   - Расчет количества дней хранения для каждого материала.
   - Определение категории запаса для каждого материала согласно шкале старения.
   - Агрегация данных по категориям (суммирование количества).
3. Формирование сводных и детальных результатов в виде графиков и таблиц.

## 8. Развертывание приложения

### Установка Conda и Python 3.10

1. **Установка Miniconda**:
   - Скачайте установщик Miniconda с [официального сайта](https://docs.conda.io/en/latest/miniconda.html)
   - Для Windows выберите инсталлятор Miniconda3 Windows 64-bit
   - Запустите скачанный файл и следуйте инструкциям установщика

2. **Создание виртуальной среды**:
   ```bash
   # Открыть командную строку или Anaconda Prompt
   conda create -n stok_env python=3.10
   ```

3. **Активация виртуальной среды**:
   ```bash
   conda activate stok_env
   ```

### Установка зависимостей и запуск приложения

1. **Клонирование репозитория**:
   ```bash
   # Создайте папку и перейдите в нее
   mkdir c:\stok
   cd c:\stok
   
   # Если используете Git
   git clone https://your-repository-url.git .
   ```

2. **Установка необходимых библиотек**:
   ```bash
   # Если у вас есть requirements.txt
   pip install -r requirements.txt
   
   # Или установка основных зависимостей вручную
   pip install streamlit pandas numpy matplotlib plotly openpyxl xlrd
   ```

3. **Запуск приложения**:
   ```bash
   # Перейдите в директорию с приложением
   cd c:\stok
   
   # Запуск приложения
   streamlit run app.py
   ```

4. **Доступ к приложению**:
   - После запуска приложение будет доступно по адресу: http://localhost:8501
   - В терминале также будет отображен URL для доступа к приложению

### Настройка для производственной среды

1. **Создание файла конфигурации**:
   Создайте файл `.streamlit/config.toml` со следующим содержимым:
   ```toml
   [server]
   port = 8501
   
   [theme]
   primaryColor = "#0078D7"
   backgroundColor = "#FFFFFF"
   secondaryBackgroundColor = "#F0F2F5"
   textColor = "#262730"
   ```

2. **Настройка для разных окружений**:
   Создайте файл `.env` для каждого окружения (dev, test, prod) с соответствующими настройками:
   ```
   # .env.dev
   DB_CONNECTION_STRING=sqlite:///dev_data.db
   
   # .env.prod
   DB_CONNECTION_STRING=postgresql://user:password@localhost:5432/stok_db
   ```

3. **Запуск для конкретного окружения**:
   ```bash
   # Для разработки
   export ENV=dev && streamlit run app.py
   
   # Для производства
   export ENV=prod && streamlit run app.py
   ```

### Обновление приложения

1. **Обновление зависимостей**:
   ```bash
   pip install -r requirements.txt --upgrade
   ```

2. **Проверка совместимости с Python 3.10**:
   Убедитесь, что все используемые библиотеки совместимы с Python 3.10.

3. **Резервное копирование данных**:
   Перед обновлением создайте резервную копию всех данных и конфигурационных файлов.
