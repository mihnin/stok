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
    sanitized = re.sub(r"[\[\]:*?/\\]", "_", sheet_name)
    return sanitized[:31]


def display_results(summary_df, detailed_df, method_name):
    """
    Display forecast results

    Args:
        summary_df: Summary forecast results
        detailed_df: Detailed forecast results
        method_name: Forecast method name
    """
    tab1, tab2, tab3 = st.tabs(["Динамика", "Сводная таблица", "Детальные результаты"])

    with tab1:
        st.markdown("### Динамика изменения объемов по категориям")
        st.markdown(
            """
            - **Падение линии КСНЗ** означает, что часть запасов перешла в СНЗ.
            - **Рост линии КСНЗ** показывает переход запасов из "Ликвидных".
            - **Преобладание СНЗ** на долгосрочном прогнозе означает, что
              большая часть запасов перейдет в "СНЗ", если не будет использована.
            """
        )
        value_column = get_value_column(summary_df)
        if not value_column:
            st.error("Не найдена колонка со значениями для графика.")
            return

        pivot_df = (
            summary_df.pivot_table(
                index="Дата прогноза",
                columns="Категория",
                values=value_column,
                aggfunc="sum",
            )
            .fillna(0)
            .reset_index()
        )

        st.session_state.pivot_df = pivot_df

        fig = create_line_chart(pivot_df, method_name, value_column)
        st.plotly_chart(fig, use_container_width=True)

        fig_area = create_area_chart(pivot_df, method_name, value_column)
        st.plotly_chart(fig_area, use_container_width=True)

    with tab2:
        st.markdown("### Сводная таблица результатов")
        display_summary_table(summary_df)

    with tab3:
        st.markdown("### Детальные результаты по материалам")
        display_detailed_table(detailed_df)

    st.markdown("### Экспорт результатов")
    add_export_button(summary_df, detailed_df)


def get_value_column(df):
    """Determine the correct value column from the DataFrame."""
    if "Оставшееся количество" in df.columns:
        return "Оставшееся количество"
    if "Фактический запас" in df.columns:
        return "Фактический запас"
    if "Количество обеспечения" in df.columns:
        return "Количество обеспечения"
    numeric_columns = df.select_dtypes(include=["number"]).columns
    return numeric_columns[0] if len(numeric_columns) > 0 else None


def create_line_chart(pivot_df, method_name, value_column):
    """Create a line chart for stock dynamics."""
    fig = go.Figure()
    categories_order = ["Ликвидный", "КСНЗ", "СНЗ", "СНЗ > 3 лет", "Требует проверки"]

    for category in categories_order:
        if category in pivot_df.columns:
            fig.add_trace(
                go.Scatter(
                    x=pivot_df["Дата прогноза"],
                    y=pivot_df[category],
                    mode="lines+markers",
                    name=category,
                    line=dict(color=COLOR_CODES.get(category, "#808080"), width=3),
                    marker=dict(size=8),
                )
            )

    fig.update_layout(
        title=f"Прогноз объемов по категориям ({method_name})",
        xaxis_title="Дата прогноза",
        yaxis_title=f"Объем запасов ({value_column})",
        legend_title="Категория",
        hovermode="x unified",
        height=600,
        template="plotly_white",
    )
    return fig


def create_area_chart(pivot_df, method_name, value_column):
    """Create an area chart for stock structure."""
    fig_area = go.Figure()
    categories_order = ["Ликвидный", "КСНЗ", "СНЗ", "СНЗ > 3 лет", "Требует проверки"]

    for category in categories_order:
        if category in pivot_df.columns:
            base_color = COLOR_CODES.get(category, "#808080")
            r, g, b = (
                int(base_color[1:3], 16),
                int(base_color[3:5], 16),
                int(base_color[5:7], 16),
            )
            rgba_color = f"rgba({r},{g},{b},0.5)"

            fig_area.add_trace(
                go.Scatter(
                    x=pivot_df["Дата прогноза"],
                    y=pivot_df[category],
                    mode="none",
                    name=category,
                    fill="tonexty",
                    fillcolor=rgba_color,
                    line=dict(width=0),
                )
            )

    fig_area.update_layout(
        title=f"Структура запасов по категориям ({method_name})",
        xaxis_title="Дата прогноза",
        yaxis_title=f"Объем запасов ({value_column})",
        legend_title="Категория",
        hovermode="x unified",
        height=500,
        template="plotly_white",
    )
    return fig_area


def display_summary_table(summary_df):
    """Display the summary results in a styled table."""
    formatted_summary = summary_df.copy()
    formatted_summary["Дата прогноза"] = formatted_summary["Дата прогноза"].dt.strftime(
        "%Y-%m-%d"
    )
    formatted_summary = formatted_summary.reset_index(drop=True)

    def color_rows(row):
        color = COLOR_CODES.get(row["Категория"], "#808080")
        text_color = "black" if row["Категория"] in ["Ликвидный", "КСНЗ"] else "white"
        return [f"background-color: {color}; color: {text_color}"] * len(row)

    st.dataframe(
        formatted_summary.style.apply(color_rows, axis=1), use_container_width=True
    )


def display_detailed_table(detailed_df):
    """Display the detailed results in a filterable, styled table."""
    all_dates = detailed_df["Дата прогноза"].dt.strftime("%Y-%m-%d").unique()
    selected_index = 0
    if st.session_state.selected_forecast_date in all_dates:
        selected_index = list(all_dates).index(st.session_state.selected_forecast_date)

    selected_date = st.selectbox(
        "Выберите дату прогноза:",
        all_dates,
        index=selected_index,
        key="forecast_date_selector",
    )
    st.session_state.selected_forecast_date = selected_date

    filtered_df = detailed_df[
        detailed_df["Дата прогноза"].dt.strftime("%Y-%m-%d") == selected_date
    ].copy()

    if "Дата поступления" in filtered_df.columns:
        filtered_df["Дата поступления"] = filtered_df["Дата поступления"].dt.strftime(
            "%Y-%m-%d"
        )
    if "Дата поступления на склад" in filtered_df.columns:
        filtered_df["Дата поступления на склад"] = filtered_df[
            "Дата поступления на склад"
        ].dt.strftime("%Y-%m-%d")

    display_cols = [c for c in filtered_df.columns if c != "Дата прогноза"]
    display_df = filtered_df[display_cols].reset_index(drop=True)

    def color_rows_detailed(row):
        color = COLOR_CODES.get(row["Категория"], "#808080")
        text_color = "black" if row["Категория"] in ["Ликвидный", "КСНЗ"] else "white"
        return [f"background-color: {color}; color: {text_color}"] * len(row)

    st.dataframe(
        display_df.style.apply(color_rows_detailed, axis=1), use_container_width=True
    )


def add_export_button(summary_df, detailed_df):
    """Add an export button to download results."""
    export_type = st.radio(
        "Формат экспорта:",
        ["Excel (все данные)", "Excel (только сводные данные)"],
        horizontal=True,
    )

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        summary_df.to_excel(writer, sheet_name="Сводные_результаты", index=False)
        if "pivot_df" in st.session_state:
            st.session_state.pivot_df.to_excel(writer, sheet_name="Сводная_таблица")

        if export_type == "Excel (все данные)":
            for date in detailed_df["Дата прогноза"].unique():
                date_str = pd.to_datetime(date).strftime("%Y-%m-%d")
                sheet_name = sanitize_excel_sheetname(f"Детали_{date_str}")
                date_df = detailed_df[detailed_df["Дата прогноза"] == date]
                date_df.to_excel(writer, sheet_name=sheet_name, index=False)

        workbook = writer.book
        worksheet = writer.sheets["Сводные_результаты"]
        for category, color in COLOR_CODES.items():
            cat_format = workbook.add_format({"bg_color": color})
            worksheet.conditional_format(
                "B2:B1000",
                {
                    "type": "text",
                    "criteria": "containing",
                    "value": category,
                    "format": cat_format,
                },
            )

    st.download_button(
        label="Скачать результаты в Excel",
        data=output.getvalue(),
        file_name=f"прогноз_{datetime.datetime.now().strftime('%Y%m%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )
