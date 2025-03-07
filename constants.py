# Константы шкалы старения для Метода 1
AGING_SCALE_METHOD_1 = [
    {"name": "< 1 месяца", "min_days": 0, "max_days": 30, "status": "Ликвидный"},
    {"name": "1-3 месяцев", "min_days": 31, "max_days": 91, "status": "Ликвидный"},
    {"name": "3-6 месяцев", "min_days": 92, "max_days": 183, "status": "Ликвидный"},
    {"name": "6-9 месяцев", "min_days": 184, "max_days": 274, "status": "Ликвидный"},
    {"name": "9-12 месяцев", "min_days": 275, "max_days": 365, "status": "КСНЗ"},
    {"name": "12-18 месяцев", "min_days": 366, "max_days": 548, "status": "СНЗ"},
    {"name": "18-24 месяца", "min_days": 549, "max_days": 730, "status": "СНЗ"},
    {"name": "2-3 года", "min_days": 731, "max_days": 1096, "status": "СНЗ"},
    {"name": "3-4 года", "min_days": 1097, "max_days": 1461, "status": "СНЗ > 3 лет"},
    {"name": "4-5 лет", "min_days": 1462, "max_days": 1826, "status": "СНЗ > 3 лет"},
    {"name": ">5 лет", "min_days": 1827, "max_days": 9999, "status": "СНЗ > 3 лет"}
]

# Константы шкалы старения для Метода 2
AGING_SCALE_METHOD_2 = [
    {"name": "< 1 месяца", "min_days": 0, "max_days": 29, "status": "Ликвидный"},
    {"name": "1 месяц", "min_days": 30, "max_days": 59, "status": "Ликвидный"},
    {"name": "2 месяца", "min_days": 60, "max_days": 90, "status": "Ликвидный"},
    {"name": "3 месяца", "min_days": 91, "max_days": 121, "status": "Ликвидный"},
    {"name": "4 месяца", "min_days": 122, "max_days": 152, "status": "Ликвидный"},
    {"name": "5 месяцев", "min_days": 153, "max_days": 182, "status": "Ликвидный"},
    {"name": "6 месяцев", "min_days": 183, "max_days": 213, "status": "Ликвидный"},
    {"name": "7 месяцев", "min_days": 214, "max_days": 244, "status": "Ликвидный"},
    {"name": "8 месяцев", "min_days": 245, "max_days": 273, "status": "Ликвидный"},
    {"name": "9 месяцев", "min_days": 274, "max_days": 304, "status": "Ликвидный"},
    {"name": "10 месяцев", "min_days": 305, "max_days": 334, "status": "КСНЗ"},
    {"name": "11 месяцев", "min_days": 335, "max_days": 364, "status": "КСНЗ"},
    {"name": "12-18 месяцев", "min_days": 365, "max_days": 547, "status": "СНЗ"},
    {"name": "18-24 месяца", "min_days": 548, "max_days": 1095, "status": "СНЗ"},
    {"name": "> 3 лет", "min_days": 1096, "max_days": 9999, "status": "СНЗ > 3 лет"},
    {"name": "Без даты", "min_days": 10000, "max_days": 99999, "status": "Требует проверки"}
]

# Константы для цветового кодирования
COLOR_CODES = {
    "Ликвидный": "#00b050",  # Зеленый
    "КСНЗ": "#ffbf00",       # Желтый
    "СНЗ": "#ff4c4c",        # Светло-красный
    "СНЗ > 3 лет": "#c00000", # Темно-красный
    "Требует проверки": "#808080"  # Серый
}

# Конфигурация колонок для методов
METHOD1_REQUIRED_COLUMNS = [
    'БЕ', 
    'Область планирования', 
    'Материал', 
    'Количество обеспечения', 
    'Дата поступления'
]

METHOD2_REQUIRED_COLUMNS = [
    'БЕ', 
    'Завод', 
    'Склад', 
    'Материал', 
    'Партия', 
    'Дата поступления на склад', 
    'Фактический запас'
]