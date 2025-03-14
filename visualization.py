import streamlit as st
import pandas as pd
import datetime
import plotly.graph_objects as go
import io
import re

from constants import COLOR_CODES

def sanitize_excel_sheetname(sheet_name):
    """
    Sanitize Excel sheet name by removing invalid characters.
    
    Args:
        sheet_name: Original sheet name
        
    Returns:
        Sanitized sheet name that is valid for Excel
    """
    # Remove invalid Excel sheet name characters: [ ] : * ? / \
    sanitized = re.sub(r'[\[\]:*?/\\]', '_', sheet_name)
    # Excel sheet names are limited to 31 characters
    return sanitized[:31]

def display_results(summary_df, detailed_df, method_name):
    """
    Display forecast results
    
    Args:
        summary_df: Summary forecast results
        detailed_df: Detailed forecast results
        method_name: Forecast method name
    """
    # Create three tabs for different result types
    tab1, tab2, tab3 = st.tabs(["Динамика запасов", "Таблица сводных результатов", "Детальные результаты"])
    
    with tab1:
        st.markdown('<h3 class="sub-header">Динамика изменения объемов по категориям</h3>', unsafe_allow_html=True)
        
        # Explanations for the charts
        st.markdown("""
        ### Пояснения к графикам:
        - **Падение линии КСНЗ** означает, что часть запасов перешла в категорию СНЗ из-за увеличения срока хранения.
        - **Рост линии КСНЗ** показывает переход запасов из категории "Ликвидный" в "Кандидаты в СНЗ".
        - **Преобладание СНЗ на долгосрочном прогнозе**: При прогнозировании на 2-3 года вперед, большая часть запасов перейдет в категории "СНЗ" и "СНЗ > 3 лет", если не будет использована.
        """, unsafe_allow_html=True)
        
        # Determine the value column based on available columns in the DataFrame
        if 'Оставшееся количество' in summary_df.columns:
            value_column = 'Оставшееся количество'
        elif 'Фактический запас' in summary_df.columns:
            value_column = 'Фактический запас'
        elif 'Количество обеспечения' in summary_df.columns:
            value_column = 'Количество обеспечения'
        else:
            # Fallback - get the first numeric column
            numeric_columns = summary_df.select_dtypes(include=['number']).columns
            if len(numeric_columns) > 0:
                value_column = numeric_columns[0]
            else:
                st.error("Не найдена подходящая колонка со значениями для графика")
                return
        
        # Prepare data for chart - ИСПРАВЛЕНО
        # Используем выбранный столбец values=value_column вместо фиксированного значения
        pivot_df = summary_df.pivot_table(
            index='Дата прогноза',
            columns='Категория',
            values=value_column,  # Используем переменную value_column
            aggfunc='sum'
        ).fillna(0).reset_index()
        
        # Store pivot_df in session state for export
        st.session_state.pivot_df = pivot_df
        
        # Create chart
        fig = go.Figure()
        
        # Add lines for each category
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
        
        # Configure chart appearance
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
        
        # Create area chart
        fig_area = go.Figure()
        
        # Add areas for each category
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
        
        # Configure chart appearance
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
        
        # Format results table
        formatted_summary = summary_df.copy()
        
        # Convert 'Forecast Date' to readable format
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
        
        # Add filter by forecast date
        all_dates = detailed_df['Дата прогноза'].dt.strftime('%Y-%m-%d').unique()
        
        # Get index of selected date
        selected_index = 0
        if st.session_state.selected_forecast_date in all_dates:
            selected_index = list(all_dates).index(st.session_state.selected_forecast_date)
        
        selected_date = st.selectbox(
            "Выберите дату прогноза:", 
            all_dates,
            index=selected_index,
            key='forecast_date_selector'
        )
        
        # Store selected date in session state
        st.session_state.selected_forecast_date = selected_date
        
        # Filter data by selected date
        filtered_df = detailed_df[detailed_df['Дата прогноза'].dt.strftime('%Y-%m-%d') == selected_date].copy()
        
        # Format date for display
        if 'Дата поступления' in filtered_df.columns:
            filtered_df['Дата поступления'] = filtered_df['Дата поступления'].dt.strftime('%Y-%m-%d')
        if 'Дата поступления на склад' in filtered_df.columns:
            filtered_df['Дата поступления на склад'] = filtered_df['Дата поступления на склад'].dt.strftime('%Y-%m-%d')
        filtered_df['Дата прогноза'] = filtered_df['Дата прогноза'].dt.strftime('%Y-%m-%d')
        
        # Remove columns that are not needed for display
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
    
    # Add export button
    st.markdown('<h3 class="sub-header">Экспорт результатов</h3>', unsafe_allow_html=True)
    
    # Instead of trying to update session state after widget creation,
    # just use the radio button directly and let Streamlit handle the state
    export_type = st.radio(
        "Формат экспорта:",
        ["Excel (все данные)", "Excel (только сводные данные)"],
        horizontal=True,
        key='export_type'
    )
    
    # Create Excel file in memory
    output = io.BytesIO()
    
    if export_type == "Excel (все данные)":
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            summary_df.to_excel(writer, sheet_name='Сводные результаты', index=False)
            
            # Split detailed results by date
            for date in detailed_df['Дата прогноза'].dt.strftime('%Y-%м-%d').unique():
                # Create sanitized sheet name
                sheet_name = sanitize_excel_sheetname(f"Детали_{date}")
                date_df = detailed_df[detailed_df['Дата прогноза'].dt.strftime('%Y-%м-%d') == date]
                date_df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            # Add pivot table
            if 'pivot_df' in st.session_state:
                st.session_state.pivot_df.to_excel(writer, sheet_name='Сводная таблица')
            
            # Configure formatting for workbook
            workbook = writer.book
            worksheet = writer.sheets['Сводные результаты']
            
            # Add formats for categories
            for category, color in COLOR_CODES.items():
                category_format = workbook.add_format({'bg_color': color})
                
                # Apply conditional formatting
                worksheet.conditional_format('B2:B1000', {'type': 'text',
                                                        'criteria': 'containing',
                                                        'value': category,
                                                        'format': category_format})
    else:
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            summary_df.to_excel(writer, sheet_name='Сводные результаты', index=False)
            
            # Add pivot table
            if 'pivot_df' in st.session_state:
                st.session_state.pivot_df.to_excel(writer, sheet_name='Сводная таблица')
            
            # Configure formatting
            workbook = writer.book
            worksheet = writer.sheets['Сводные результаты']
            
            for category, color in COLOR_CODES.items():
                category_format = workbook.add_format({'bg_color': color})
                worksheet.conditional_format('B2:B1000', {'type': 'text',
                                                        'criteria': 'containing',
                                                        'value': category,
                                                        'format': category_format})
    
    # Offer file for download
    st.download_button(
        label="Скачать результаты в Excel",
        data=output.getvalue(),
        file_name=f"прогноз_снз_кснз_{datetime.datetime.now().strftime('%Y-%m-%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )