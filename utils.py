import pandas as pd
import datetime
from constants import AGING_SCALE_METHOD_1, AGING_SCALE_METHOD_2

def calculate_aging_days(receipt_date, forecast_date=None):
    """
    Расчет количества дней хранения запаса
    
    Args:
        receipt_date: Дата поступления на склад
        forecast_date: Дата прогноза (если None, используется текущая дата)
    
    Returns:
        int: Количество дней хранения
    """
    if pd.isna(receipt_date):
        return 10000  # Специальный код для запасов без даты
    
    if forecast_date is None:
        forecast_date = datetime.datetime.now().date()
    elif isinstance(forecast_date, str):
        forecast_date = pd.to_datetime(forecast_date).date()
    
    if isinstance(receipt_date, str):
        receipt_date = pd.to_datetime(receipt_date).date()
    
    return (forecast_date - receipt_date).days

def determine_aging_category(days, method=1):
    """
    Определение категории запаса по количеству дней хранения
    
    Args:
        days: Количество дней хранения
        method: Метод расчета (1 или 2)
    
    Returns:
        dict: Информация о категории запаса
    """
    aging_scale = AGING_SCALE_METHOD_1 if method == 1 else AGING_SCALE_METHOD_2
    
    for category in aging_scale:
        if category["min_days"] <= days <= category["max_days"]:
            return category
    
    # Если ни в одну категорию не попали (что странно)
    return {"name": "Неопределено", "status": "Требует проверки"}

def validate_columns(df, required_columns):
    """
    Проверка наличия необходимых колонок в DataFrame
    
    Args:
        df: DataFrame для проверки
        required_columns: Список обязательных колонок
    
    Returns:
        tuple: (bool, list) - Результат проверки и список отсутствующих колонок
    """
    missing_columns = [col for col in required_columns if col not in df.columns]
    return (len(missing_columns) == 0, missing_columns)

def generate_sample_data_method1():
    """
    Генерация тестовых данных для Метода 1
    
    Returns:
        DataFrame: Тестовые данные
    """
    data = {
        'БЕ': ['0101', '0101', '0101', '0101', '0101'],
        'Область планирования': ['1000', '1000', '1000', '1000', '1000'],
        'Материал': ['100001', '100002', '100003', '100004', '100005'],
        'Количество обеспечения': [100, 200, 150, 300, 250],
        'Дата поступления': [
            (datetime.datetime.now() - datetime.timedelta(days=400)).strftime('%Y-%m-%d'),
            (datetime.datetime.now() - datetime.timedelta(days=300)).strftime('%Y-%m-%d'),
            (datetime.datetime.now() - datetime.timedelta(days=200)).strftime('%Y-%m-%d'),
            (datetime.datetime.now() - datetime.timedelta(days=100)).strftime('%Y-%m-%d'),
            (datetime.datetime.now() - datetime.timedelta(days=50)).strftime('%Y-%m-%d'),
        ],
        'Дневное потребление': [0.5, 0.2, 0.1, 0.3, 0.0]
    }
    return pd.DataFrame(data)

def generate_sample_data_method2():
    """
    Генерация тестовых данных для Метода 2
    
    Returns:
        DataFrame: Тестовые данные
    """
    data = {
        'БЕ': ['0101', '0101', '0101', '0101', '0101'],
        'Завод': ['1111', '1111', '1111', '1111', '1111'],
        'Склад': ['1111', '1111', '1111', '1111', '1111'],
        'Материал': ['200001', '200002', '200003', '200004', '200005'],
        'Партия': ['0000000001', '0000000002', '0000000003', '0000000004', '0000000005'],
        'СПП элемент': ['', '', '', '', ''],
        'Дата поступления на склад': [
            (datetime.datetime.now() - datetime.timedelta(days=400)).strftime('%Y-%m-%d'),
            (datetime.datetime.now() - datetime.timedelta(days=300)).strftime('%Y-%m-%d'),
            (datetime.datetime.now() - datetime.timedelta(days=200)).strftime('%Y-%m-%d'),
            (datetime.datetime.now() - datetime.timedelta(days=100)).strftime('%Y-%m-%d'),
            (datetime.datetime.now() - datetime.timedelta(days=50)).strftime('%Y-%m-%d'),
        ],
        'Фактический запас': [100, 200, 150, 300, 250]
    }
    return pd.DataFrame(data)