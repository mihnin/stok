def generate_sample_data_method1():
    """
    Генерация тестовых данных для Метода 1 (1000 записей)
    
    Returns:
        DataFrame: Тестовые данные
    """
    import numpy as np
    
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

def generate_sample_data_method2():
    """
    Генерация тестовых данных для Метода 2 (1000 записей)
    
    Returns:
        DataFrame: Тестовые данные
    """
    import numpy as np
    
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