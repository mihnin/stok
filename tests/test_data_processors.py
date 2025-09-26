import pandas as pd
import pytest
from datetime import datetime, timedelta
from data_processors import (
    forecast_with_demand,
    handle_materials_without_date,
    handle_mixed_batches,
)

# Фиксированная дата для предсказуемости тестов
TODAY = datetime(2023, 10, 27)


@pytest.fixture
def mixed_batch_data():
    """Фикстура для тестирования обработки смешанных партий."""
    return pd.DataFrame(
        {
            "БЕ": ["0101", "0101", "0101", "0101"],
            "Завод": ["1111", "1111", "1111", "1111"],
            "Склад": ["2222", "2222", "2222", "2222"],
            "Материал": ["M1", "M1", "M2", "M2"],
            "Партия": ["P1", "P1", "P2", "P2"],
            "СПП элемент": ["", "", "", ""],
            "Дата поступления на склад": [
                TODAY - timedelta(days=10),  # M1, P1 -> Ликвидный
                TODAY - timedelta(days=310),  # M1, P1 -> КСНЗ
                TODAY - timedelta(days=20),  # M2, P2 -> Ликвидный
                TODAY - timedelta(days=30),  # M2, P2 -> Ликвидный
            ],
            "Фактический запас": [10, 20, 30, 40],
        }
    )


def test_handle_mixed_batches_logic(mixed_batch_data):
    """
    Проверяет, что партии корректно разделяются или объединяются
    в зависимости от их категории старения.
    """
    processed_df = handle_mixed_batches(mixed_batch_data, current_date=TODAY)

    assert len(processed_df) == 3

    m1_df = processed_df[processed_df["Материал"] == "M1"]
    assert len(m1_df) == 2
    assert 10 in m1_df["Фактический запас"].values
    assert 20 in m1_df["Фактический запас"].values

    m2_df = processed_df[processed_df["Материал"] == "M2"]
    assert len(m2_df) == 1
    assert m2_df.iloc[0]["Фактический запас"] == 70


def test_handle_materials_without_date():
    """Проверяет корректную обработку материалов без даты."""
    data = pd.DataFrame(
        {
            "Дата поступления на склад": [TODAY, pd.NaT, TODAY - timedelta(days=1)],
            "Фактический запас": [100, 50, 100],
            "БЕ": ["01", "02", "03"],
            "Завод": ["A", "B", "C"],
            "Склад": ["S1", "S2", "S3"],
            "Материал": ["M1", "M2", "M3"],
            "Партия": ["P1", "P2", "P3"],
            "СПП элемент": ["", "", ""],
        }
    )
    processed_df = handle_materials_without_date(data)
    assert processed_df.loc[1, "Категория"] == "Требует проверки"
    assert processed_df.loc[1, "Дни хранения"] == 10000
    assert "Категория" not in processed_df.columns or pd.isna(
        processed_df.loc[0, "Категория"]
    )


@pytest.fixture
def forecast_data():
    """Фикстура для тестирования логики прогнозирования."""
    return pd.DataFrame(
        {
            "БЕ": ["0101", "0101", "0101"],
            "Область планирования": ["1001", "1001", "1001"],
            "Материал": ["M_LIQ", "M_KSNZ", "M_SNZ"],
            "Количество обеспечения": [100, 50, 20],
            "Дата поступления": [
                TODAY - timedelta(days=10),  # Ликвидный
                TODAY - timedelta(days=270),  # Станет КСНЗ через 5 дней
                TODAY - timedelta(days=361),  # Станет СНЗ через 5 дней (361+5=366)
            ],
        }
    )


def test_forecast_with_demand_category_progression(forecast_data):
    """Проверяет корректный переход материалов по категориям со временем."""
    end_date = TODAY + timedelta(days=6)
    summary_df, details_df = forecast_with_demand(
        forecast_data, end_date, step_days=5, current_date=TODAY
    )

    day1 = details_df[details_df["Дата прогноза"] == pd.to_datetime(TODAY)]
    assert day1[day1["Материал"] == "M_LIQ"].iloc[0]["Категория"] == "Ликвидный"
    assert day1[day1["Материал"] == "M_KSNZ"].iloc[0]["Категория"] == "Ликвидный"
    assert day1[day1["Материал"] == "M_SNZ"].iloc[0]["Категория"] == "КСНЗ"

    day2_date = pd.to_datetime(TODAY + timedelta(days=5))
    day2 = details_df[details_df["Дата прогноза"] == day2_date]
    assert day2[day2["Материал"] == "M_LIQ"].iloc[0]["Категория"] == "Ликвидный"
    assert day2[day2["Материал"] == "M_KSNZ"].iloc[0]["Категория"] == "КСНЗ"
    assert day2[day2["Материал"] == "M_SNZ"].iloc[0]["Категория"] == "СНЗ"

    day2_summary = summary_df[summary_df["Дата прогноза"] == day2_date]
    liq_sum = day2_summary[day2_summary["Категория"] == "Ликвидный"]
    ksnz_sum = day2_summary[day2_summary["Категория"] == "КСНЗ"]
    snz_sum = day2_summary[day2_summary["Категория"] == "СНЗ"]
    assert liq_sum.iloc[0]["Количество обеспечения"] == 100
    assert ksnz_sum.iloc[0]["Количество обеспечения"] == 50
    assert snz_sum.iloc[0]["Количество обеспечения"] == 20
