# ex2.py
import pandas as pd
import datetime
import os
import numpy as np

def generate_sample_data_method2():
    """
    Генерация тестовых данных для Метода 2 (1000 записей)
    
    Returns:
        DataFrame: Тестовые данные
    """
    # Создаем базовые данные
    be_list = ['0101', '0102', '0103', '0104', '0105']
    plant_list = ['1111', '2222', '3333', '4444', '5555']
    storage_list = ['1111', '2222', '3333', '4444', '5555']
    material_prefix_list = ['100', '200', '300', '400', '500']
    
    # Генерируем 1000 записей
    n_records = 1000
    data = {
        'БЕ': [],
        'Завод': [],
        'Склад': [],
        'Материал': [],
        'Партия': [],
        'СПП элемент': [],
        'Дата поступления на склад': [],
        'Фактический запас': []
    }
    
    # Сегодняшний день
    today = datetime.datetime.now()
    
    # Заполняем данные
    for i in range(n_records):
        # Выбираем БЕ, завод и склад
        be_idx = i % len(be_list)
        plant_idx = i % len(plant_list)
        storage_idx = i % len(storage_list)
        
        # Генерируем материал и партию
        material = f"{material_prefix_list[i % len(material_prefix_list)]}{i:04d}"
        batch = f"{plant_list[plant_idx]}{i:07d}"
        
        # Генерируем СПП элемент (может быть пустым)
        spp_element = "" if np.random.random() < 0.7 else f"SPP{i:05d}"
        
        # Генерируем количество (от 10 до 1000)
        quantity = np.random.randint(10, 1001)
        
        # Генерируем дату поступления (от 2 лет назад до сегодня)
        days_ago = np.random.randint(0, 730)  # До 2 лет назад
        date = (today - datetime.timedelta(days=days_ago)).strftime('%Y-%m-%d')
        
        # Добавляем данные
        data['БЕ'].append(be_list[be_idx])
        data['Завод'].append(plant_list[plant_idx])
        data['Склад'].append(storage_list[storage_idx])
        data['Материал'].append(material)
        data['Партия'].append(batch)
        data['СПП элемент'].append(spp_element)
        data['Дата поступления на склад'].append(date)
        data['Фактический запас'].append(quantity)
    
    return pd.DataFrame(data)

# Генерация тестовых данных для Метода 2
df_method2 = generate_sample_data_method2()

# Сохранение в Excel
if not os.path.exists('sample_data'):
    os.makedirs('sample_data')
    
df_method2.to_excel('sample_data/method2_sample.xlsx', index=False)
print("Файл сохранен: sample_data/method2_sample.xlsx")