import pytest
import pandas as pd
import plotly.graph_objects as go
from visualization import (
    sanitize_excel_sheetname,
    get_value_column,
    create_line_chart,
    create_area_chart,
)


@pytest.mark.parametrize(
    "input_name, expected_name",
    [
        ("ValidName", "ValidName"),
        ("Invalid[Name]", "Invalid_Name_"),
        ("A*B?C/D\\E:F", "A_B_C_D_E_F"),
        (
            "ThisIsAVeryLongSheetNameThatWillBeTruncated",
            "ThisIsAVeryLongSheetNameThatWil",
        ),
    ],
)
def test_sanitize_excel_sheetname(input_name, expected_name):
    """Test sanitization of Excel sheet names."""
    assert sanitize_excel_sheetname(input_name) == expected_name


@pytest.mark.parametrize(
    "columns, expected",
    [
        (["Количество обеспечения", "Другое"], "Количество обеспечения"),
        (["Фактический запас", "Количество обеспечения"], "Фактический запас"),
        (["Оставшееся количество", "Фактический запас"], "Оставшееся количество"),
        (["A", "B", "Numeric"], "Numeric"),
        (["X", "Y", "Z"], None),
    ],
)
def test_get_value_column(columns, expected):
    """Test the logic for selecting the correct value column."""
    data = {col: [1] if col == "Numeric" else ["text"] for col in columns}
    df = pd.DataFrame(data)
    # For non-numeric test cases, convert to numeric where expected
    if expected and expected not in ["A", "B", "C", "X", "Y", "Z"]:
        df[expected] = [100]

    assert get_value_column(df) == expected


@pytest.fixture
def chart_data():
    """Fixture for chart creation tests."""
    return pd.DataFrame(
        {
            "Дата прогноза": pd.to_datetime(["2023-01-01", "2023-01-02"]),
            "Ликвидный": [100, 90],
            "КСНЗ": [10, 20],
            "СНЗ": [5, 5],
        }
    )


def test_create_line_chart(chart_data):
    """Test that the line chart is created with correct properties."""
    fig = create_line_chart(chart_data, "Метод 1", "Количество")
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 3  # Three traces for 3 categories
    trace_names = [trace.name for trace in fig.data]
    assert "Ликвидный" in trace_names
    assert "КСНЗ" in trace_names
    assert "СНЗ" in trace_names


def test_create_area_chart(chart_data):
    """Test that the area chart is created with correct properties."""
    fig = create_area_chart(chart_data, "Метод 2", "Запас")
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 3
    trace_names = [trace.name for trace in fig.data]
    assert "Ликвидный" in trace_names
    assert "КСНЗ" in trace_names
    assert "СНЗ" in trace_names
    assert fig.data[0].fill == "tonexty"  # Check if it's an area chart
