# ex1.py
import pandas as pd
import datetime
import os
import numpy as np

def generate_sample_data_method1():
    """
    Генерация тестовых данных для Метода 1 (1000 записей)
    
    Returns:
        DataFrame: Тестовые данные
    """
    # Создаем базовые данные
    be_list = ['0101', '0102', '0103', '0104', '0105']
    area_list = ['1000', '2000', '3000', '4000', '5000']
    material_prefix_list = ['100', '200', '300', '400', '500']
    
    # Генерируем 1000 записей
    n_records = 1000
    data = {
        'БЕ': [],
        'Область планирования': [],
        'Материал': [],
        'Количество обеспечения': [],
        'Дата поступления': [],
        'Дневное потребление': []
    }
    
    # Сегодняшний день
    today = datetime.datetime.now()
    
    # Заполняем данные
    for i in range(n_records):
        # Выбираем БЕ и область планирования
        be_idx = i % len(be_list)
        area_idx = i % len(area_list)
        
        # Генерируем материал
        material = f"{material_prefix_list[i % len(material_prefix_list)]}{i:04d}"
        
        # Генерируем количество обеспечения (от 10 до 1000)
        quantity = np.random.randint(10, 1001)
        
        # Генерируем дату поступления (от 1 года назад до сегодня)
        days_ago = np.random.randint(0, 730)  # До 2 лет назад
        date = (today - datetime.timedelta(days=days_ago)).strftime('%Y-%m-%d')
        
        # Генерируем дневное потребление (от 0 до 1, с вероятностью 0 - 30%)
        if np.random.random() < 0.3:
            consumption = 0.0
        else:
            consumption = np.round(np.random.random() * quantity / 365, 2)  # Примерно годовое потребление

        # Добавляем данные
        data['БЕ'].append(be_list[be_idx])
        data['Область планирования'].append(area_list[area_idx])
        data['Материал'].append(material)
        data['Количество обеспечения'].append(quantity)
        data['Дата поступления'].append(date)
        data['Дневное потребление'].append(consumption)
    
    return pd.DataFrame(data)

# Генерация тестовых данных для Метода 1
df_method1 = generate_sample_data_method1()

# Сохранение в Excel
if not os.path.exists('sample_data'):
    os.makedirs('sample_data')
    
df_method1.to_excel('sample_data/method1_sample.xlsx', index=False)
print("Файл сохранен: sample_data/method1_sample.xlsx")