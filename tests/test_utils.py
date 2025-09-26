import pandas as pd
import pytest
from datetime import datetime, timedelta
from utils import (
    validate_columns,
    calculate_aging_days,
    determine_aging_category,
)


def test_validate_columns_success():
    """Test that validate_columns returns True when all columns are present."""
    df = pd.DataFrame({"A": [1], "B": [2], "C": [3]})
    required_columns = ["A", "B"]
    is_valid, missing = validate_columns(df, required_columns)
    assert is_valid is True
    assert len(missing) == 0


def test_validate_columns_failure():
    """Test that validate_columns returns False and the missing columns."""
    df = pd.DataFrame({"A": [1], "B": [2]})
    required_columns = ["A", "C"]
    is_valid, missing = validate_columns(df, required_columns)
    assert is_valid is False
    assert missing == ["C"]


def test_validate_columns_empty_df():
    """Test validate_columns with an empty DataFrame."""
    df = pd.DataFrame()
    required_columns = ["A", "B"]
    is_valid, missing = validate_columns(df, required_columns)
    assert is_valid is False
    assert sorted(missing) == sorted(["A", "B"])


def test_calculate_aging_days_basic():
    """Test the basic calculation of day difference."""
    forecast_date = datetime(2023, 1, 31)
    entry_date = datetime(2023, 1, 1)
    days = calculate_aging_days(entry_date, forecast_date)
    assert days == 30


def test_calculate_aging_days_no_forecast_date():
    """Test calculation against the current date if forecast_date is not set."""
    entry_date = datetime.now() - timedelta(days=10)
    days = calculate_aging_days(entry_date)
    assert days == 10


def test_calculate_aging_days_na_date():
    """Test that a null date returns the special value."""
    days = calculate_aging_days(pd.NaT)
    assert days == 10000


@pytest.mark.parametrize(
    "days, expected_category",
    [
        (10, "Ликвидный"),
        (274, "Ликвидный"),
        (275, "КСНЗ"),
        (365, "КСНЗ"),
        (366, "СНЗ"),
        (1096, "СНЗ"),
        (1097, "СНЗ > 3 лет"),
        (9999, "СНЗ > 3 лет"),
    ],
)
def test_determine_aging_category_method1(days, expected_category):
    """Test category determination for Method 1."""
    category_info = determine_aging_category(days, method=1)
    assert category_info["status"] == expected_category


@pytest.mark.parametrize(
    "days, expected_category",
    [
        (100, "Ликвидный"),
        (304, "Ликвидный"),
        (305, "КСНЗ"),
        (364, "КСНЗ"),
        (365, "СНЗ"),
        (1095, "СНЗ"),
        (1096, "СНЗ > 3 лет"),
        (9999, "СНЗ > 3 лет"),
    ],
)
def test_determine_aging_category_method2(days, expected_category):
    """Test category determination for Method 2."""
    category_info = determine_aging_category(days, method=2)
    assert category_info["status"] == expected_category


def test_determine_aging_category_out_of_bounds():
    """Test that a very large number of days falls into the last category."""
    category_info = determine_aging_category(20000, method=1)
    assert category_info["status"] == "СНЗ > 3 лет"
    category_info = determine_aging_category(20000, method=2)
    assert category_info["status"] == "СНЗ > 3 лет"
