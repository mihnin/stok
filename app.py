import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import plotly.graph_objects as go
import io
import os
import base64

from constants import COLOR_CODES, METHOD1_REQUIRED_COLUMNS, METHOD2_REQUIRED_COLUMNS
from utils import validate_columns, generate_sample_data_method1, generate_sample_data_method2
from data_processors import (
    forecast_with_demand,
    forecast_without_demand,
    handle_materials_without_date,
    handle_mixed_batches
)
from visualization import display_results
#from documentation import get_documentation_content

def initialize_session_state():
    """Initialize session state variables if they don't exist"""
    if 'uploaded_data' not in st.session_state:
        st.session_state.uploaded_data = None
    
    if 'forecast_summary' not in st.session_state:
        st.session_state.forecast_summary = None
    
    if 'forecast_details' not in st.session_state:
        st.session_state.forecast_details = None
        
    if 'forecast_method' not in st.session_state:
        st.session_state.forecast_method = "Метод 1: С учетом потребности"
    
    if 'forecast_enddate' not in st.session_state:
        st.session_state.forecast_enddate = datetime.datetime.now().date() + datetime.timedelta(days=365)
    
    if 'forecast_step' not in st.session_state:
        st.session_state.forecast_step = 30
        
    if 'data_source' not in st.session_state:
        st.session_state.data_source = "Загрузить Excel файл"
        
    if 'selected_forecast_date' not in st.session_state:
        st.session_state.selected_forecast_date = None
        
    if 'export_type' not in st.session_state:
        st.session_state.export_type = "Excel (все данные)"
        
    if 'last_uploaded_file' not in st.session_state:
        st.session_state.last_uploaded_file = None

def on_method_change():
    """Reset uploaded data when method changes"""
    st.session_state.uploaded_data = None
    st.session_state.forecast_summary = None
    st.session_state.forecast_details = None
    st.session_state.selected_forecast_date = None

def on_file_upload():
    """Handle file upload"""
    return

def main():
    st.set_page_config(
        page_title="Система прогнозирования СНЗ и КСНЗ",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Apply CSS
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #2B5797;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2B5797;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .status-box {
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .status-likvid {
        background-color: #00b050;
        color: white;
    }
    .status-ksnz {
        background-color: #ffbf00;
        color: black;
    }
    .status-snz {
        background-color: #ff4c4c;
        color: white;
    }
    .status-snz3 {
        background-color: #c00000;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main content - removed tabs and documentation
    st.markdown('<h1 class="main-header">Система прогнозирования сверхнормативных запасов (СНЗ и КСНЗ)</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.subheader("Параметры прогнозирования")
        
        # Method selection with callback
        method = st.radio(
            "Метод прогнозирования:",
            [
                "Метод 1: С учетом потребности",
                "Метод 2: Без учета потребности (только фактический запас)"
            ],
            on_change=on_method_change,
            key="forecast_method"
        )
        
        # Show appropriate template info based on selected method
        if "Метод 1" in method:
            st.info("Для данного метода используйте шаблон для Метода 1 (с учетом потребности)")
        else:
            st.info("Для данного метода используйте шаблон для Метода 2 (без учета потребности)")
        
        data_source = st.radio(
            "Источник данных:",
            [
                "Загрузить Excel файл",
                "Использовать тестовые данные"
            ],
            key="data_source"
        )
        
        if data_source == "Загрузить Excel файл":
            uploaded_file = st.file_uploader(
                "Загрузите Excel файл с данными",
                type=["xlsx", "xls"],
                key="file_uploader"
            )
            
            if uploaded_file is not None:
                try:
                    df = pd.read_excel(uploaded_file)
                    st.session_state.uploaded_data = df
                except Exception as e:
                    st.error(f"Ошибка при загрузке файла: {str(e)}")
        
        today = datetime.datetime.now().date()
        end_date = st.date_input(
            "Дата окончания прогноза:",
            value=st.session_state.forecast_enddate,
            min_value=today,
            max_value=today + datetime.timedelta(days=1825),  # Max 5 years
            key="forecast_enddate"
        )
        
        step_days = st.number_input(
            "Шаг прогноза (дни):",
            min_value=1,
            max_value=90,
            value=st.session_state.forecast_step,
            key="forecast_step"
        )
        
        st.markdown("---")
        
        st.markdown("""
        ### Условные обозначения:
        <div class="status-box status-likvid">Ликвидный запас</div>
        <div class="status-box status-ksnz">КСНЗ (Критический сверхнормативный запас)</div>
        <div class="status-box status-snz">СНЗ (Сверхнормативный запас)</div>
        <div class="status-box status-snz3">СНЗ > 3 лет</div>
        """, unsafe_allow_html=True)
        
        run_forecast = st.button("Рассчитать прогноз", type="primary", use_container_width=True)
        
        # Sample data download
        st.markdown("---")
        st.subheader("Шаблоны данных")
        
        # Create sample data directory if it doesn't exist
        if not os.path.exists('sample_data'):
            os.makedirs('sample_data')
        
        col1, col2 = st.columns(2)
        with col1:
            # Generate sample data if not exists
            if not os.path.exists('sample_data/method1_sample.xlsx'):
                sample_df1 = generate_sample_data_method1()
                sample_df1.to_excel('sample_data/method1_sample.xlsx', index=False)
            
            st.download_button(
                label="Шаблон для Метода 1",
                data=open('sample_data/method1_sample.xlsx', 'rb').read(),
                file_name="шаблон_метод1.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        with col2:
            if not os.path.exists('sample_data/method2_sample.xlsx'):
                sample_df2 = generate_sample_data_method2()
                sample_df2.to_excel('sample_data/method2_sample.xlsx', index=False)
            
            st.download_button(
                label="Шаблон для Метода 2",
                data=open('sample_data/method2_sample.xlsx', 'rb').read(),
                file_name="шаблон_метод2.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
    # Define data source
    df = None
    
    if data_source == "Использовать тестовые данные":
        if "Метод 1" in method:
            df = generate_sample_data_method1()
            st.session_state.uploaded_data = df
            st.info("Используются тестовые данные для Метода 1")
        else:
            df = generate_sample_data_method2()
            st.session_state.uploaded_data = df
            st.info("Используются тестовые данные для Метода 2")
    elif data_source == "Загрузить Excel файл" and st.session_state.uploaded_data is not None:
        df = st.session_state.uploaded_data
        st.success(f"Файл успешно загружен. Количество строк: {len(df)}")
    
    # Main panel
    if df is not None:
        # Display loaded data
        st.markdown('<h2 class="sub-header">Исходные данные</h2>', unsafe_allow_html=True)
        
        with st.expander("Просмотр исходных данных", expanded=False):
            st.dataframe(df, use_container_width=True)
        
        # Check if uploaded file matches selected method
        if "Метод 1" in method:
            valid, missing_columns = validate_columns(df, METHOD1_REQUIRED_COLUMNS)
            if not valid:
                st.error(f"Загруженный файл не соответствует Методу 1. Отсутствуют обязательные колонки: {', '.join(missing_columns)}")
                st.warning("Пожалуйста, загрузите файл, соответствующий выбранному методу")
                df = None
        else:
            valid, missing_columns = validate_columns(df, METHOD2_REQUIRED_COLUMNS)
            if not valid:
                st.error(f"Загруженный файл не соответствует Методу 2. Отсутствуют обязательные колонки: {', '.join(missing_columns)}")
                st.warning("Пожалуйста, загрузите файл, соответствующий выбранному методу")
                df = None
        
        if df is not None and run_forecast:
            st.markdown('<h2 class="sub-header">Результаты прогнозирования</h2>', unsafe_allow_html=True)
            
            if "Метод 1" in method:
                # If no daily consumption column, create it with zeros
                if 'Дневное потребление' not in df.columns:
                    st.warning("Колонка 'Дневное потребление' отсутствует. Добавлена с нулевыми значениями.")
                    df['Дневное потребление'] = 0
                
                with st.spinner("Выполняется прогнозирование..."):
                    # Run forecast
                    summary_results, detailed_results = forecast_with_demand(df, end_date, step_days)
                    
                    # Save results to session state
                    st.session_state.forecast_summary = summary_results
                    st.session_state.forecast_details = detailed_results
                    
                    # Set initial selected date if not already set
                    if st.session_state.selected_forecast_date is None:
                        all_dates = detailed_results['Дата прогноза'].dt.strftime('%Y-%m-%d').unique()
                        if len(all_dates) > 0:
                            st.session_state.selected_forecast_date = all_dates[0]
                
                # Display results
                display_results(summary_results, detailed_results, "Метод 1")
                
            else:  # Method 2
                with st.spinner("Выполняется прогнозирование..."):
                    # Handle special cases
                    df = handle_materials_without_date(df)
                    df = handle_mixed_batches(df)
                    
                    # Run forecast
                    summary_results, detailed_results = forecast_without_demand(df, end_date, step_days)
                    
                    # Save results to session state
                    st.session_state.forecast_summary = summary_results
                    st.session_state.forecast_details = detailed_results
                    
                    # Set initial selected date if not already set
                    if st.session_state.selected_forecast_date is None:
                        all_dates = detailed_results['Дата прогноза'].dt.strftime('%Y-%m-%d').unique()
                        if len(all_dates) > 0:
                            st.session_state.selected_forecast_date = all_dates[0]
                
                # Display results
                display_results(summary_results, detailed_results, "Метод 2")
        
        # Display previous forecast results if they exist
        elif st.session_state.forecast_summary is not None and st.session_state.forecast_details is not None:
            st.markdown('<h2 class="sub-header">Результаты прогнозирования</h2>', unsafe_allow_html=True)
            display_results(st.session_state.forecast_summary, st.session_state.forecast_details, 
                            "Метод 1" if "Метод 1" in method else "Метод 2")
    else:
        if data_source == "Загрузить Excel файл":
            st.info("Пожалуйста, загрузите Excel файл для начала работы.")

if __name__ == "__main__":
    main()