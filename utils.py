import pandas as pd
import datetime
from constants import AGING_SCALE_METHOD_1, AGING_SCALE_METHOD_2


def validate_columns(df, required_columns):
    """
    Проверяет наличие всех необходимых столбцов в датафрейме.

    Args:
        df (pandas.DataFrame): Датафрейм для проверки
        required_columns (list): Список обязательных столбцов

    Returns:
        tuple: (valid, missing_columns)
    """
    existing_columns = set(df.columns)
    required_set = set(required_columns)
    missing_columns = list(required_set - existing_columns)

    return len(missing_columns) == 0, missing_columns


def calculate_aging_days(date, forecast_date=None):
    """
    Расчет количества дней хранения

    Args:
        date: Дата поступления материала
        forecast_date: Дата прогноза (по умолчанию сегодня)

    Returns:
        int: Количество дней хранения
    """
    if forecast_date is None:
        forecast_date = datetime.datetime.now()

    if pd.isna(date):
        return 10000  # Специальное значение для материалов без даты

    return (forecast_date - pd.to_datetime(date)).days


def determine_aging_category(days, method=1):
    """
    Определение категории старения на основе дней хранения

    Args:
        days: Количество дней хранения
        method: Метод прогнозирования (1 или 2)

    Returns:
        dict: Информация о категории старения
    """
    scale = AGING_SCALE_METHOD_1 if method == 1 else AGING_SCALE_METHOD_2

    for category in scale:
        if category["min_days"] <= days <= category["max_days"]:
            return category

    return scale[-1]


def generate_sample_data_method1():
    """
    Генерирует пример данных для метода 1 (с учетом потребности)

    Returns:
        pandas.DataFrame: Датафрейм с примером данных
    """
    today = datetime.datetime.now().date()
    dates = [
        today - datetime.timedelta(days=10),
        today - datetime.timedelta(days=100),
        today - datetime.timedelta(days=200),
        today - datetime.timedelta(days=300),
        today - datetime.timedelta(days=400),
        today - datetime.timedelta(days=800),
        today - datetime.timedelta(days=1100),
    ]
    data = {
        "БЕ": ["0101", "0101", "0101", "0102", "0102", "0103", "0103"],
        "Область планирования": [
            "1001",
            "1001",
            "1002",
            "1002",
            "1003",
            "1003",
            "1004",
        ],
        "Материал": [
            "10000001",
            "10000002",
            "10000003",
            "10000004",
            "10000005",
            "10000006",
            "10000007",
        ],
        "Количество обеспечения": [100, 150, 200, 120, 80, 90, 60],
        "Дата поступления": dates,
        "Дневное потребление": [0.5, 0.3, 0.1, 0.05, 0.2, 0.0, 0.0],
    }
    return pd.DataFrame(data)


def generate_sample_data_method2():
    """
    Генерирует пример данных для метода 2 (без учета потребности)

    Returns:
        pandas.DataFrame: Датафрейм с примером данных
    """
    today = datetime.datetime.now().date()
    dates = [
        today - datetime.timedelta(days=15),
        today - datetime.timedelta(days=120),
        today - datetime.timedelta(days=250),
        today - datetime.timedelta(days=320),
        today - datetime.timedelta(days=400),
        today - datetime.timedelta(days=800),
        today - datetime.timedelta(days=1100),
        None,
    ]
    data = {
        "БЕ": ["0101", "0101", "0101", "0102", "0102", "0103", "0103", "0104"],
        "Завод": ["1001", "1001", "1002", "1002", "1003", "1003", "1004", "1005"],
        "Склад": ["2001", "2001", "2002", "2002", "2003", "2003", "2004", "2005"],
        "Материал": [
            "20000001",
            "20000002",
            "20000003",
            "20000004",
            "20000005",
            "20000006",
            "20000007",
            "20000008",
        ],
        "Партия": ["A001", "A002", "A003", "A004", "A005", "A006", "A007", "A008"],
        "СПП элемент": ["", "", "SP001", "", "SP002", "", "", ""],
        "Дата поступления на склад": dates,
        "Фактический запас": [100, 150, 200, 120, 80, 90, 60, 40],
    }
    return pd.DataFrame(data)
