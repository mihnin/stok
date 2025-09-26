# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Streamlit-based stock forecasting application** for predicting excessive inventory (СНЗ и КСНЗ) in warehouse management. The application analyzes stock aging patterns and forecasts when materials will transition between liquid stock, candidates for excessive stock (КСНЗ), and excessive stock (СНЗ) categories.

## Key Development Commands

### Running the Application
```bash
streamlit run app.py
```
The application will be available at http://localhost:8501

### Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_data_processors.py
pytest tests/test_utils.py
pytest tests/test_visualization.py

# Run with verbose output
pytest -v
```

### Code Quality
```bash
# Lint code
flake8

# Format code
black .
```

### Dependencies
```bash
# Install requirements
pip install -r requirements.txt

# Key dependencies: streamlit, pandas, numpy, plotly, openpyxl
```

## Architecture Overview

The application follows a modular architecture with clear separation of concerns:

### Core Modules

- **`app.py`** - Main Streamlit application entry point, handles UI and user interactions
- **`data_processors.py`** - Core forecasting algorithms for both Method 1 (with demand) and Method 2 (without demand)
- **`visualization.py`** - Chart generation and results display using Plotly
- **`utils.py`** - Utility functions for data validation, aging calculations, and sample data generation
- **`constants.py`** - Configuration constants including aging scales, color codes, and required columns
- **`help.py`** - Help documentation and user guidance

### Data Processing Flow

1. **Data Input**: Excel file upload or sample data generation
2. **Validation**: Column validation using `validate_columns()` from utils.py
3. **Processing**: Two forecasting methods:
   - Method 1: `forecast_with_demand()` - Uses "Количество обеспечения" from ZMML_REP_RD report
   - Method 2: `forecast_without_demand()` - Uses only actual stock ("Фактический запас")
4. **Categorization**: Materials classified using aging scales from constants.py
5. **Visualization**: Results displayed using visualization.py functions

### Key Forecasting Logic

The application uses two different aging scales (METHOD 1 vs METHOD 2) defined in constants.py:
- **Method 1**: Liquid stock < 275 days, КСНЗ 275-365 days, СНЗ 366+ days
- **Method 2**: Liquid stock < 305 days, КСНЗ 305-365 days, СНЗ 365+ days

Stock categories are color-coded consistently throughout the application using COLOR_CODES from constants.py.

## Data Requirements

### Method 1 (ZMML_REP_RD Report)
Required columns: БЕ, Область планирования, Материал, Количество обеспечения, Дата поступления

### Method 2 (Actual Stock Only)
Required columns: БЕ, Завод, Склад, Материал, Партия, Дата поступления на склад, Фактический запас

## Coding Guidelines

Based on `.github/copilot-instructions.md`:
- All code must be in English (variables, functions, classes)
- Comments may be in Russian
- Prefer simple solutions and avoid code duplication
- Keep files under 200-300 lines
- Write thorough tests for major functionality
- Focus only on areas relevant to the current task

## Session State Management

The application uses Streamlit's session state to maintain:
- `uploaded_data` - Current dataset
- `forecast_summary` - Aggregated forecast results
- `forecast_details` - Detailed forecast data
- `forecast_method` - Selected forecasting method
- Various UI state variables

## Testing Strategy

Tests are organized by module:
- `test_data_processors.py` - Core forecasting algorithm tests
- `test_utils.py` - Utility function tests
- `test_visualization.py` - Chart generation tests

All tests use pytest framework and include both unit tests and integration tests with sample data.