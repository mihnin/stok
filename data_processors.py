import pandas as pd
import datetime
from utils import calculate_aging_days, determine_aging_category

def forecast_with_demand(df, forecast_end_date, step_days=30):
    """
    Прогнозирование запасов с учетом потребности
    
    Args:
        df: DataFrame с данными о запасах и потреблении
        forecast_end_date: Конечная дата прогноза
        step_days: Шаг прогноза в днях
    
    Returns:
        DataFrame: Прогноз состояния запасов на каждую дату
    """
    # Конвертация дат в datetime
    df['Дата поступления'] = pd.to_datetime(df['Дата поступления'])
    forecast_end_date = pd.to_datetime(forecast_end_date)
    
    # Генерация дат прогноза
    current_date = datetime.datetime.now()
    dates = pd.date_range(start=current_date, end=forecast_end_date, freq=f'{step_days}D')
    
    # Создаем пустой список для результатов
    forecast_results = []
    
    # Детальные результаты по каждому материалу
    detailed_forecast = []
    
    for forecast_date in dates:
        # Копируем исходные данные
        temp_df = df.copy()
        
        # Расчет дней хранения для текущей даты прогноза
        temp_df['Дни хранения'] = temp_df['Дата поступления'].apply(
            lambda x: calculate_aging_days(x, forecast_date)
        )
        
        # Расчет оставшегося количества с учетом потребления
        # Предполагаем, что есть колонка 'Дневное потребление'
        days_from_now = (forecast_date - current_date).days
        temp_df['Оставшееся количество'] = temp_df['Количество обеспечения'] - \
                                          (temp_df['Дневное потребление'] * days_from_now)
        temp_df['Оставшееся количество'] = temp_df['Оставшееся количество'].clip(lower=0)
        
        # Определение категории для каждой строки
        temp_df['Категория'] = temp_df['Дни хранения'].apply(
            lambda x: determine_aging_category(x, method=1)['status']
        )
        
        # Сохраняем детальные данные для каждой даты прогноза
        temp_df['Дата прогноза'] = forecast_date
        detailed_forecast.append(temp_df)
        
        # Агрегация по категориям
        summary = temp_df.groupby('Категория')['Оставшееся количество'].sum().reset_index()
        summary['Дата прогноза'] = forecast_date
        
        forecast_results.append(summary)
    
    # Объединяем все результаты
    summary_df = pd.concat(forecast_results)
    detailed_df = pd.concat(detailed_forecast)
    
    return summary_df, detailed_df

def forecast_without_demand(df, forecast_end_date, step_days=30):
    """
    Прогнозирование запасов без учета потребности
    
    Args:
        df: DataFrame с данными о запасах
        forecast_end_date: Конечная дата прогноза
        step_days: Шаг прогноза в днях
    
    Returns:
        DataFrame: Прогноз состояния запасов на каждую дату
    """
    # Конвертация дат в datetime
    df['Дата поступления на склад'] = pd.to_datetime(df['Дата поступления на склад'])
    forecast_end_date = pd.to_datetime(forecast_end_date)
    
    # Генерация дат прогноза
    current_date = datetime.datetime.now()
    dates = pd.date_range(start=current_date, end=forecast_end_date, freq=f'{step_days}D')
    
    # Создаем пустой список для результатов
    forecast_results = []
    
    # Детальные результаты по каждому материалу
    detailed_forecast = []
    
    for forecast_date in dates:
        # Копируем исходные данные
        temp_df = df.copy()
        
        # Расчет дней хранения для текущей даты прогноза
        temp_df['Дни хранения'] = temp_df['Дата поступления на склад'].apply(
            lambda x: calculate_aging_days(x, forecast_date)
        )
        
        # Определение категории для каждой строки
        temp_df['Категория'] = temp_df['Дни хранения'].apply(
            lambda x: determine_aging_category(x, method=2)['status']
        )
        
        # Сохраняем детальные данные для каждой даты прогноза
        temp_df['Дата прогноза'] = forecast_date
        detailed_forecast.append(temp_df)
        
        # Агрегация по категориям
        summary = temp_df.groupby('Категория')['Фактический запас'].sum().reset_index()
        summary['Дата прогноза'] = forecast_date
        
        forecast_results.append(summary)
    
    # Объединяем все результаты
    summary_df = pd.concat(forecast_results)
    detailed_df = pd.concat(detailed_forecast)
    
    return summary_df, detailed_df

def handle_mixed_batches(df):
    """
    Обработка партий с разными датами поступления
    
    Args:
        df: DataFrame с данными о запасах
    
    Returns:
        DataFrame: Обработанные данные
    """
    # Группировка по ключевым полям партии
    batch_groups = df.groupby(['БЕ', 'Завод', 'Склад', 'Материал', 'Партия', 'СПП элемент'])
    
    processed_data = []
    
    for name, group in batch_groups:
        if len(group) > 1:
            # Если есть несколько записей для одной партии с разными датами
            # Сортируем по дате (более новые даты первыми)
            sorted_group = group.sort_values('Дата поступления на склад', ascending=False)
            
            # Проверяем наличие разных категорий в группе
            categories = []
            for _, row in sorted_group.iterrows():
                days = calculate_aging_days(row['Дата поступления на склад'])
                category = determine_aging_category(days, method=2)['status']
                if category not in categories:
                    categories.append(category)
            
            if len(categories) > 1:
                # Если есть разные категории, создаем отдельные записи по категориям
                for category in categories:
                    # Выбираем записи с этой категорией
                    category_rows = []
                    remaining_qty = 0
                    
                    for _, row in sorted_group.iterrows():
                        days = calculate_aging_days(row['Дата поступления на склад'])
                        row_category = determine_aging_category(days, method=2)['status']
                        
                        if row_category == category:
                            category_rows.append(row)
                            remaining_qty += row['Фактический запас']
                    
                    if category_rows:
                        # Создаем новую запись с суммарным количеством
                        new_row = category_rows[0].copy()
                        new_row['Фактический запас'] = remaining_qty
                        processed_data.append(new_row)
            else:
                # Если все записи в одной категории, объединяем их
                new_row = sorted_group.iloc[0].copy()
                new_row['Фактический запас'] = sorted_group['Фактический запас'].sum()
                processed_data.append(new_row)
        else:
            # Если только одна запись, добавляем как есть
            processed_data.append(group.iloc[0])
    
    return pd.DataFrame(processed_data)

def handle_materials_without_date(df):
    """
    Обработка материалов без даты поступления
    
    Args:
        df: DataFrame с данными о запасах
    
    Returns:
        DataFrame: Обработанные данные
    """
    # Находим записи без даты
    no_date_mask = df['Дата поступления на склад'].isna()
    
    if no_date_mask.any():
        # Копируем DataFrame для модификации
        result_df = df.copy()
        
        # Устанавливаем специальную категорию для записей без даты
        result_df.loc[no_date_mask, 'Категория'] = 'Требует проверки'
        result_df.loc[no_date_mask, 'Дни хранения'] = 10000
        
        return result_df
    else:
        return df