import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import plotly.graph_objects as go
import io
import os

from constants import COLOR_CODES, METHOD1_REQUIRED_COLUMNS, METHOD2_REQUIRED_COLUMNS
from utils import validate_columns, generate_sample_data_method1, generate_sample_data_method2
from data_processors import (
    forecast_with_demand,
    forecast_without_demand,
    handle_materials_without_date,
    handle_mixed_batches
)

def main():
    st.set_page_config(
        page_title="Система прогнозирования СНЗ и КСНЗ",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Настройка темы
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
    
    st.markdown('<h1 class="main-header">Система прогнозирования сверхнормативных запасов (СНЗ и КСНЗ)</h1>', unsafe_allow_html=True)
    
    # Боковая панель для загрузки файлов и настройки параметров
    with st.sidebar:
        st.subheader("Параметры прогнозирования")
        
        method = st.radio(
            "Метод прогнозирования:",
            [
                "Метод 1: С учетом потребности",
                "Метод 2: Без учета потребности (только фактический запас)"
            ]
        )
        
        data_source = st.radio(
            "Источник данных:",
            [
                "Загрузить Excel файл",
                "Использовать тестовые данные"
            ]
        )
        
        if data_source == "Загрузить Excel файл":
            uploaded_file = st.file_uploader(
                "Загрузите Excel файл с данными",
                type=["xlsx", "xls"]
            )
        
        today = datetime.datetime.now().date()
        end_date = st.date_input(
            "Дата окончания прогноза:",
            value=today + datetime.timedelta(days=365),
            min_value=today,
            max_value=today + datetime.timedelta(days=1825)  # Максимум 5 лет
        )
        
        step_days = st.number_input(
            "Шаг прогноза (дни):",
            min_value=1,
            max_value=90,
            value=30
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
    
    # Определение источника данных
    df = None
    
    if data_source == "Использовать тестовые данные":
        if "Метод 1" in method:
            df = generate_sample_data_method1()
            st.info("Используются тестовые данные для Метода 1")
        else:
            df = generate_sample_data_method2()
            st.info("Используются тестовые данные для Метода 2")
    elif data_source == "Загрузить Excel файл" and uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            st.success(f"Файл успешно загружен. Количество строк: {len(df)}")
        except Exception as e:
            st.error(f"Ошибка при загрузке файла: {str(e)}")
    
    # Основная панель
    if df is not None:
        # Отображение загруженных данных
        st.markdown('<h2 class="sub-header">Исходные данные</h2>', unsafe_allow_html=True)
        
        with st.expander("Просмотр исходных данных", expanded=False):
            st.dataframe(df, use_container_width=True)
        
        if run_forecast:
            st.markdown('<h2 class="sub-header">Результаты прогнозирования</h2>', unsafe_allow_html=True)
            
            if "Метод 1" in method:
                # Проверка необходимых колонок для Метода 1
                valid, missing_columns = validate_columns(df, METHOD1_REQUIRED_COLUMNS)
                
                if not valid:
                    st.error(f"Отсутствуют обязательные колонки: {', '.join(missing_columns)}")
                else:
                    # Если нет колонки с дневным потреблением, создаем ее с нулевыми значениями
                    if 'Дневное потребление' not in df.columns:
                        st.warning("Колонка 'Дневное потребление' отсутствует. Добавлена с нулевыми значениями.")
                        df['Дневное потребление'] = 0
                    
                    with st.spinner("Выполняется прогнозирование..."):
                        # Выполнение прогноза
                        summary_results, detailed_results = forecast_with_demand(df, end_date, step_days)
                    
                    # Отображение результатов
                    display_results(summary_results, detailed_results, "Метод 1")
                    
            else:  # Метод 2
                # Проверка необходимых колонок для Метода 2
                valid, missing_columns = validate_columns(df, METHOD2_REQUIRED_COLUMNS)
                
                if not valid:
                    st.error(f"Отсутствуют обязательные колонки: {', '.join(missing_columns)}")
                else:
                    with st.spinner("Выполняется прогнозирование..."):
                        # Обработка особых случаев
                        df = handle_materials_without_date(df)
                        df = handle_mixed_batches(df)
                        
                        # Выполнение прогноза
                        summary_results, detailed_results = forecast_without_demand(df, end_date, step_days)
                    
                    # Отображение результатов
                    display_results(summary_results, detailed_results, "Метод 2")
    else:
        if data_source == "Загрузить Excel файл":
            st.info("Пожалуйста, загрузите Excel файл для начала работы.")

def display_results(summary_df, detailed_df, method_name):
    """
    Отображение результатов прогнозирования
    
    Args:
        summary_df: Сводные результаты прогноза
        detailed_df: Детальные результаты прогноза
        method_name: Название метода прогнозирования
    """
    # Создание трех вкладок для разных типов результатов
    tab1, tab2, tab3 = st.tabs(["Динамика запасов", "Таблица сводных результатов", "Детальные результаты"])
    
    with tab1:
        st.markdown('<h3 class="sub-header">Динамика изменения объемов по категориям</h3>', unsafe_allow_html=True)
        
        # Подготовка данных для графика
        value_column = 'Оставшееся количество' if 'Оставшееся количество' in summary_df.columns else 'Фактический запас'
        
        pivot_df = summary_df.pivot_table(
            index='Дата прогноза',
            columns='Категория',
            values=value_column,
            aggfunc='sum'
        ).fillna(0).reset_index()
        
        # Создание графика
        fig = go.Figure()
        
        # Добавление линий для каждой категории
        categories_order = ["Ликвидный", "КСНЗ", "СНЗ", "СНЗ > 3 лет", "Требует проверки"]
        
        for category in categories_order:
            if category in pivot_df.columns:
                fig.add_trace(go.Scatter(
                    x=pivot_df['Дата прогноза'],
                    y=pivot_df[category],
                    mode='lines+markers',
                    name=category,
                    line=dict(color=COLOR_CODES.get(category, '#808080'), width=3),
                    marker=dict(size=8)
                ))
        
        # Настройка внешнего вида графика
        fig.update_layout(
            title=f"Прогноз изменения объемов запасов по категориям ({method_name})",
            xaxis_title="Дата прогноза",
            yaxis_title=f"Объем запасов ({value_column})",
            legend_title="Категория запаса",
            hovermode="x unified",
            height=600,
            template="plotly_white"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Создание графика в виде области
        fig_area = go.Figure()
        
        # Добавление областей для каждой категории
        for category in categories_order:
            if category in pivot_df.columns:
                # Use rgba() format for colors with transparency
                base_color = COLOR_CODES.get(category, '#808080')
                # Convert hex to rgba with 0.5 opacity
                if base_color.startswith('#'):
                    r = int(base_color[1:3], 16)
                    g = int(base_color[3:5], 16)
                    b = int(base_color[5:7], 16)
                    rgba_color = f'rgba({r},{g},{b},0.5)'
                else:
                    rgba_color = base_color
                
                fig_area.add_trace(go.Scatter(
                    x=pivot_df['Дата прогноза'],
                    y=pivot_df[category],
                    mode='none',
                    name=category,
                    fill='tonexty',
                    fillcolor=rgba_color,
                    line=dict(width=0)
                ))
        
        # Настройка внешнего вида графика
        fig_area.update_layout(
            title=f"Структура запасов по категориям ({method_name})",
            xaxis_title="Дата прогноза",
            yaxis_title=f"Объем запасов ({value_column})",
            legend_title="Категория запаса",
            hovermode="x unified",
            height=500,
            template="plotly_white"
        )
        
        st.plotly_chart(fig_area, use_container_width=True)
    
    with tab2:
        st.markdown('<h3 class="sub-header">Сводная таблица результатов прогноза</h3>', unsafe_allow_html=True)
        
        # Форматирование таблицы с результатами
        formatted_summary = summary_df.copy()
        
        # Преобразовать 'Дата прогноза' в читаемый формат
        formatted_summary['Дата прогноза'] = formatted_summary['Дата прогноза'].dt.strftime('%Y-%m-%d')
        
        # Ensure unique index for styling
        formatted_summary = formatted_summary.reset_index(drop=True)
        
        # Create a color mapping for each row based on category
        def color_rows(row):
            color = COLOR_CODES.get(row['Категория'], '#808080')
            text_color = 'black' if row['Категория'] in ['Ликвидный', 'КСНЗ'] else 'white'
            return [f'background-color: {color}; color: {text_color}'] * len(row)
        
        # Display with styling
        st.dataframe(formatted_summary.style.apply(color_rows, axis=1), use_container_width=True)
    
    with tab3:
        st.markdown('<h3 class="sub-header">Детальные результаты по материалам</h3>', unsafe_allow_html=True)
        
        # Добавляем фильтр по дате прогноза
        all_dates = detailed_df['Дата прогноза'].dt.strftime('%Y-%m-%d').unique()
        selected_date = st.selectbox("Выберите дату прогноза:", all_dates)
        
        # Фильтруем данные по выбранной дате
        filtered_df = detailed_df[detailed_df['Дата прогноза'].dt.strftime('%Y-%m-%d') == selected_date].copy()
        
        # Форматирование даты для отображения
        if 'Дата поступления' in filtered_df.columns:
            filtered_df['Дата поступления'] = filtered_df['Дата поступления'].dt.strftime('%Y-%m-%d')
        if 'Дата поступления на склад' in filtered_df.columns:
            filtered_df['Дата поступления на склад'] = filtered_df['Дата поступления на склад'].dt.strftime('%Y-%m-%d')
        filtered_df['Дата прогноза'] = filtered_df['Дата прогноза'].dt.strftime('%Y-%m-%d')
        
        # Удаляем колонки, которые не нужны для отображения
        display_columns = [col for col in filtered_df.columns if col not in ['Дата прогноза']]
        
        # Ensure unique index for styling
        display_df = filtered_df[display_columns].reset_index(drop=True)
        
        # Create a color mapping for each row based on category
        def color_rows_detailed(row):
            color = COLOR_CODES.get(row['Категория'], '#808080')
            text_color = 'black' if row['Категория'] in ['Ликвидный', 'КСНЗ'] else 'white'
            return [f'background-color: {color}; color: {text_color}'] * len(row)
            
        # Display with styling
        st.dataframe(display_df.style.apply(color_rows_detailed, axis=1), use_container_width=True)
    
    # Добавляем кнопку экспорта результатов
    st.markdown('<h3 class="sub-header">Экспорт результатов</h3>', unsafe_allow_html=True)
    
    export_type = st.radio(
        "Формат экспорта:",
        ["Excel (все данные)", "Excel (только сводные данные)"],
        horizontal=True
    )
    
    # Создаем Excel файл в памяти
    output = io.BytesIO()
    
    if export_type == "Excel (все данные)":
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            summary_df.to_excel(writer, sheet_name='Сводные результаты', index=False)
            
            # Разбиваем детальные результаты по датам
            for date in detailed_df['Дата прогноза'].dt.strftime('%Y-%m-%d').unique():
                sheet_name = f"Детали_{date}"
                date_df = detailed_df[detailed_df['Дата прогноза'].dt.strftime('%Y-%m-%d') == date]
                date_df.to_excel(writer, sheet_name=sheet_name[:31], index=False)  # Excel ограничивает имя листа 31 символом
            
            # Добавляем сводную таблицу
            pivot_df.to_excel(writer, sheet_name='Сводная таблица')
            
            # Настройка форматирования для рабочей книги
            workbook = writer.book
            worksheet = writer.sheets['Сводные результаты']
            
            # Добавляем форматы для категорий
            for category, color in COLOR_CODES.items():
                category_format = workbook.add_format({'bg_color': color})
                
                # Применяем условное форматирование
                worksheet.conditional_format('B2:B1000', {'type': 'text',
                                                        'criteria': 'containing',
                                                        'value': category,
                                                        'format': category_format})
    else:
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            summary_df.to_excel(writer, sheet_name='Сводные результаты', index=False)
            pivot_df.to_excel(writer, sheet_name='Сводная таблица')
            
            # Настройка форматирования
            workbook = writer.book
            worksheet = writer.sheets['Сводные результаты']
            
            for category, color in COLOR_CODES.items():
                category_format = workbook.add_format({'bg_color': color})
                worksheet.conditional_format('B2:B1000', {'type': 'text',
                                                        'criteria': 'containing',
                                                        'value': category,
                                                        'format': category_format})
    
    # Предлагаем скачать файл
    st.download_button(
        label="Скачать результаты в Excel",
        data=output.getvalue(),
        file_name=f"прогноз_снз_кснз_{datetime.datetime.now().strftime('%Y-%m-%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

if __name__ == "__main__":
    main()