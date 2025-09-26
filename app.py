import streamlit as st
import pandas as pd
import datetime
import os

from constants import METHOD1_REQUIRED_COLUMNS, METHOD2_REQUIRED_COLUMNS
from utils import (
    validate_columns,
    generate_sample_data_method1,
    generate_sample_data_method2,
)
from data_processors import (
    forecast_with_demand,
    forecast_without_demand,
    handle_materials_without_date,
    handle_mixed_batches,
)
from visualization import display_results
from help import show_help_page

EXCEL_MIME_TYPE = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


def initialize_session_state():
    """Initialize session state variables if they don't exist"""
    if "uploaded_data" not in st.session_state:
        st.session_state.uploaded_data = None

    if "forecast_summary" not in st.session_state:
        st.session_state.forecast_summary = None

    if "forecast_details" not in st.session_state:
        st.session_state.forecast_details = None

    if "forecast_method" not in st.session_state:
        st.session_state.forecast_method = "Метод 1: С учетом потребности"

    if "forecast_enddate" not in st.session_state:
        st.session_state.forecast_enddate = (
            datetime.datetime.now().date() + datetime.timedelta(days=365)
        )

    if "forecast_step" not in st.session_state:
        st.session_state.forecast_step = 30

    if "data_source" not in st.session_state:
        st.session_state.data_source = "Загрузить Excel файл"

    if "selected_forecast_date" not in st.session_state:
        st.session_state.selected_forecast_date = None

    if "export_type" not in st.session_state:
        st.session_state.export_type = "Excel (все данные)"

    if "last_uploaded_file" not in st.session_state:
        st.session_state.last_uploaded_file = None

    if "show_help" not in st.session_state:
        st.session_state.show_help = False


def toggle_help():
    """Toggle the help screen display state."""
    st.session_state.show_help = not st.session_state.show_help


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
        initial_sidebar_state="expanded",
    )

    initialize_session_state()

    st.markdown(
        """
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
    /* ... other styles ... */
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<h1 class="main-header">Прогноз СНЗ и КСНЗ</h1>', unsafe_allow_html=True
    )

    with st.sidebar:
        help_col1, help_col2 = st.columns([1, 1])
        with help_col1:
            st.button(
                "📚 Справка" if not st.session_state.show_help else "🔙 Назад",
                on_click=toggle_help,
                key="help_button",
                use_container_width=True,
            )

        with help_col2:
            if os.path.exists("documentation/user_guide.pdf"):
                st.download_button(
                    label="📥 Скачать руководство",
                    data=open("documentation/user_guide.pdf", "rb").read(),
                    file_name="руководство_пользователя.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )

        st.markdown("---")

        if not st.session_state.show_help:
            st.subheader("Параметры прогнозирования")

            method = st.radio(
                "Метод прогнозирования:",
                [
                    "Метод 1: С учетом потребности",
                    "Метод 2: Без учета потребности (только фактический запас)",
                ],
                on_change=on_method_change,
                key="forecast_method",
            )

            if "Метод 1" in method:
                st.info("Используйте шаблон для Метода 1 (с потребностью)")
            else:
                st.info("Используйте шаблон для Метода 2 (без потребности)")

            data_source = st.radio(
                "Источник данных:",
                ["Загрузить Excel файл", "Использовать тестовые данные"],
                key="data_source",
            )

            if data_source == "Загрузить Excel файл":
                uploaded_file = st.file_uploader(
                    "Загрузите Excel файл", type=["xlsx", "xls"], key="file_uploader"
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
                max_value=today + datetime.timedelta(days=1825),
                key="forecast_enddate",
            )

            step_days = st.number_input(
                "Шаг прогноза (дни):",
                1,
                90,
                value=st.session_state.forecast_step,
                key="forecast_step",
            )

            st.markdown("---")
            run_forecast = st.button(
                "Рассчитать прогноз", type="primary", use_container_width=True
            )

            st.markdown("---")
            st.subheader("Шаблоны данных")

            if not os.path.exists("sample_data"):
                os.makedirs("sample_data")

            col1, col2 = st.columns(2)
            with col1:
                if not os.path.exists("sample_data/method1_sample.xlsx"):
                    sample_df1 = generate_sample_data_method1()
                    sample_df1.to_excel("sample_data/method1_sample.xlsx", index=False)

                st.download_button(
                    label="Шаблон для Метода 1",
                    data=open("sample_data/method1_sample.xlsx", "rb").read(),
                    file_name="шаблон_метод1.xlsx",
                    mime=EXCEL_MIME_TYPE,
                )

            with col2:
                if not os.path.exists("sample_data/method2_sample.xlsx"):
                    sample_df2 = generate_sample_data_method2()
                    sample_df2.to_excel("sample_data/method2_sample.xlsx", index=False)

                st.download_button(
                    label="Шаблон для Метода 2",
                    data=open("sample_data/method2_sample.xlsx", "rb").read(),
                    file_name="шаблон_метод2.xlsx",
                    mime=EXCEL_MIME_TYPE,
                )

    if st.session_state.show_help:
        show_help_page()
    else:
        df = None
        if data_source == "Использовать тестовые данные":
            if "Метод 1" in method:
                df = generate_sample_data_method1()
            else:
                df = generate_sample_data_method2()
            st.session_state.uploaded_data = df
            st.info(f"Используются тестовые данные для {method}")
        elif st.session_state.uploaded_data is not None:
            df = st.session_state.uploaded_data
            st.success(f"Файл загружен. Строк: {len(df)}")

        if df is not None:
            st.markdown(
                '<h2 class="sub-header">Исходные данные</h2>', unsafe_allow_html=True
            )
            with st.expander("Просмотр исходных данных", expanded=False):
                st.dataframe(df, use_container_width=True)

            required_cols = (
                METHOD1_REQUIRED_COLUMNS
                if "Метод 1" in method
                else METHOD2_REQUIRED_COLUMNS
            )
            valid, missing = validate_columns(df, required_cols)
            if not valid:
                st.error(f"Неверный формат. Нет колонок: {', '.join(missing)}")
                df = None

            if df is not None and run_forecast:
                st.markdown(
                    '<h2 class="sub-header">Результаты</h2>', unsafe_allow_html=True
                )
                with st.spinner("Выполняется прогнозирование..."):
                    if "Метод 1" in method:
                        summary, details = forecast_with_demand(df, end_date, step_days)
                    else:  # Method 2
                        df = handle_materials_without_date(df)
                        df = handle_mixed_batches(df)
                        summary, details = forecast_without_demand(
                            df, end_date, step_days
                        )

                    st.session_state.forecast_summary = summary
                    st.session_state.forecast_details = details
                    if (
                        st.session_state.selected_forecast_date is None
                        and not details.empty
                    ):
                        all_dates = details["Дата прогноза"].unique()
                        if len(all_dates) > 0:
                            st.session_state.selected_forecast_date = all_dates[0]

                if not summary.empty:
                    display_results(summary, details, method)

            elif st.session_state.forecast_summary is not None:
                st.markdown(
                    '<h2 class="sub-header">Результаты</h2>', unsafe_allow_html=True
                )
                display_results(
                    st.session_state.forecast_summary,
                    st.session_state.forecast_details,
                    method,
                )
        else:
            if data_source == "Загрузить Excel файл":
                st.info("Пожалуйста, загрузите Excel файл для начала работы.")


if __name__ == "__main__":
    main()
