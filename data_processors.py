import pandas as pd
import datetime
from utils import calculate_aging_days, determine_aging_category


def forecast_with_demand(df, forecast_end_date, step_days=30, current_date=None):
    """
    Прогнозирование запасов с учетом потребности.

    Args:
        df: DataFrame с данными о запасах и потреблении.
        forecast_end_date: Конечная дата прогноза.
        step_days: Шаг прогноза в днях.
        current_date: Дата, от которой начинается прогноз (для тестирования).

    Returns:
        tuple: Два DataFrame (сводный и детальный).
    """
    df["Дата поступления"] = pd.to_datetime(df["Дата поступления"])
    forecast_end_date = pd.to_datetime(forecast_end_date)

    if current_date is None:
        current_date = datetime.datetime.now()

    dates = pd.date_range(
        start=current_date, end=forecast_end_date, freq=f"{step_days}D"
    )

    detailed_results = []
    for forecast_date in dates:
        temp_df = df.copy()
        temp_df["Дни хранения"] = temp_df["Дата поступления"].apply(
            lambda x: calculate_aging_days(x, forecast_date)
        )
        temp_df["Категория"] = temp_df["Дни хранения"].apply(
            lambda x: determine_aging_category(x, method=1)["status"]
        )
        temp_df["Дата прогноза"] = forecast_date
        detailed_results.append(temp_df)

    if not detailed_results:
        return pd.DataFrame(), pd.DataFrame()

    detailed_df = pd.concat(detailed_results, ignore_index=True)
    summary_df = (
        detailed_df.groupby(["Дата прогноза", "Категория"])["Количество обеспечения"]
        .sum()
        .reset_index()
    )
    return summary_df, detailed_df


def forecast_without_demand(df, forecast_end_date, step_days=30, current_date=None):
    """
    Прогнозирование запасов без учета потребности.

    Args:
        df: DataFrame с данными о запасах.
        forecast_end_date: Конечная дата прогноза.
        step_days: Шаг прогноза в днях.
        current_date: Дата, от которой начинается прогноз (для тестирования).

    Returns:
        tuple: Два DataFrame (сводный и детальный).
    """
    df["Дата поступления на склад"] = pd.to_datetime(df["Дата поступления на склад"])
    forecast_end_date = pd.to_datetime(forecast_end_date)

    if current_date is None:
        current_date = datetime.datetime.now()

    dates = pd.date_range(
        start=current_date, end=forecast_end_date, freq=f"{step_days}D"
    )

    detailed_results = []
    for forecast_date in dates:
        temp_df = df.copy()
        temp_df["Дни хранения"] = temp_df["Дата поступления на склад"].apply(
            lambda x: calculate_aging_days(x, forecast_date)
        )
        temp_df["Категория"] = temp_df["Дни хранения"].apply(
            lambda x: determine_aging_category(x, method=2)["status"]
        )
        temp_df["Дата прогноза"] = forecast_date
        detailed_results.append(temp_df)

    if not detailed_results:
        return pd.DataFrame(), pd.DataFrame()

    detailed_df = pd.concat(detailed_results, ignore_index=True)
    summary_df = (
        detailed_df.groupby(["Дата прогноза", "Категория"])["Фактический запас"]
        .sum()
        .reset_index()
    )
    return summary_df, detailed_df


def handle_mixed_batches(df, current_date=None):
    """
    Обработка партий с разными датами поступления.

    Args:
        df (pd.DataFrame): DataFrame с данными о запасах.
        current_date (datetime, optional): Текущая дата для расчета.

    Returns:
        pd.DataFrame: Обработанные данные.
    """
    if current_date is None:
        current_date = datetime.datetime.now()

    processed_rows = []
    group_cols = ["БЕ", "Завод", "Склад", "Материал", "Партия", "СПП элемент"]
    for _, group in df.groupby(group_cols):
        if len(group) > 1:
            group["temp_category"] = group["Дата поступления на склад"].apply(
                lambda x: determine_aging_category(
                    calculate_aging_days(x, current_date), method=2
                )["status"]
            )
            if group["temp_category"].nunique() > 1:
                for category, cat_group in group.groupby("temp_category"):
                    new_row = cat_group.iloc[0].copy()
                    new_row["Фактический запас"] = cat_group["Фактический запас"].sum()
                    processed_rows.append(new_row)
            else:
                new_row = group.iloc[0].copy()
                new_row["Фактический запас"] = group["Фактический запас"].sum()
                processed_rows.append(new_row)
        else:
            processed_rows.append(group.iloc[0])

    if not processed_rows:
        return pd.DataFrame(columns=df.columns)

    result_df = pd.DataFrame(processed_rows).reset_index(drop=True)
    if "temp_category" in result_df.columns:
        result_df = result_df.drop(columns=["temp_category"])
    return result_df


def handle_materials_without_date(df):
    """
    Обработка материалов без даты поступления.

    Args:
        df: DataFrame с данными о запасах.

    Returns:
        DataFrame: Обработанные данные.
    """
    no_date_mask = df["Дата поступления на склад"].isna()
    if no_date_mask.any():
        result_df = df.copy()
        result_df.loc[no_date_mask, "Категория"] = "Требует проверки"
        result_df.loc[no_date_mask, "Дни хранения"] = 10000
        return result_df
    return df
