import streamlit as st

def get_documentation_content():
    """
    Возвращает HTML содержимое документации для использования в Streamlit.
    
    Returns:
        str: HTML строка с содержимым документации.
    """
    return """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Руководство пользователя системы прогнозирования СНЗ и КСНЗ</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 {
            color: #2B5797;
            text-align: center;
            margin-bottom: 30px;
        }
        h2 {
            color: #2B5797;
            margin-top: 40px;
            border-bottom: 1px solid #ddd;
            padding-bottom: 10px;
        }
        h3 {
            color: #2B5797;
            margin-top: 25px;
        }
        h4 {
            margin-top: 20px;
        }
        .content {
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .toc {
            background-color: #f5f5f5;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 30px;
        }
        .toc ol {
            margin-left: 20px;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        .status-box {
            padding: 8px 12px;
            border-radius: 3px;
            font-weight: bold;
            text-align: center;
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
        .status-check {
            background-color: #808080;
            color: white;
        }
        pre {
            background-color: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            font-family: Consolas, monospace;
            margin: 15px 0;
        }
        .code-block {
            background-color: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
        }
        .color-sample {
            display: inline-block;
            width: 20px;
            height: 20px;
            vertical-align: middle;
            margin-right: 10px;
            border-radius: 3px;
        }
        .note {
            background-color: #e7f3fe;
            border-left: 6px solid #2196F3;
            padding: 15px;
            margin: 15px 0;
        }
        .warning {
            background-color: #fff9e6;
            border-left: 6px solid #ffbf00;
            padding: 15px;
            margin: 15px 0;
        }
    </style>
</head>
<body>
    <h1>Система прогнозирования сверхнормативных запасов (СНЗ и КСНЗ)</h1>

    <div class="toc">
        <h2 id="contents">Содержание</h2>
        <ol>
            <li><a href="#overview">Общее описание системы</a></li>
            <li><a href="#methods">Методы прогнозирования</a></li>
            <li><a href="#data-preparation">Подготовка данных</a></li>
            <li><a href="#app-usage">Работа с приложением</a></li>
            <li><a href="#results">Интерпретация результатов</a></li>
            <li><a href="#edge-cases">Особые случаи и обработка исключений</a></li>
            <li><a href="#formulas">Формулы и алгоритмы расчета</a></li>
        </ol>
    </div>
    
    <h2 id="overview">1. Общее описание системы</h2>
    <div class="content">
        <p>Система прогнозирования сверхнормативных запасов (СНЗ и КСНЗ) предназначена для анализа и прогнозирования уровня складских запасов, 
        которые в будущем могут быть квалифицированы как критические (КСНЗ) или сверхнормативные (СНЗ).</p>
        
        <p>Система позволяет определить, когда конкретный материал перейдет в статус КСНЗ или СНЗ, если не будет использован, 
        что дает возможность заблаговременно принять меры по вовлечению материала в производство, предотвращая его переход в категорию неликвидов.</p>
        
        <h3>Основные понятия и категории запасов:</h3>
        <table>
            <tr>
                <th>Категория</th>
                <th>Описание</th>
                <th>Цветовое обозначение</th>
            </tr>
            <tr>
                <td><span class="status-box status-likvid">Ликвидный запас</span></td>
                <td>Запас, хранящийся на складе менее определенного периода (обычно до 9 месяцев для Метода 1 и до 10 месяцев для Метода 2).</td>
                <td><span class="color-sample" style="background-color: #00b050;"></span> Зеленый</td>
            </tr>
            <tr>
                <td><span class="status-box status-ksnz">КСНЗ</span></td>
                <td>Критический сверхнормативный запас — запас, который находится на грани перехода в сверхнормативный (обычно от 9-10 месяцев до 1 года).</td>
                <td><span class="color-sample" style="background-color: #ffbf00;"></span> Желтый</td>
            </tr>
            <tr>
                <td><span class="status-box status-snz">СНЗ</span></td>
                <td>Сверхнормативный запас — запас, хранящийся на складе дольше допустимого срока (более 1 года до 3 лет).</td>
                <td><span class="color-sample" style="background-color: #ff4c4c;"></span> Красный</td>
            </tr>
            <tr>
                <td><span class="status-box status-snz3">СНЗ > 3 лет</span></td>
                <td>Запас, хранящийся на складе более 3 лет, который с высокой вероятностью требует списания.</td>
                <td><span class="color-sample" style="background-color: #c00000;"></span> Темно-красный</td>
            </tr>
            <tr>
                <td><span class="status-box status-check">Требует проверки</span></td>
                <td>Запасы без указанной даты поступления, которые требуют дополнительной проверки и уточнения данных.</td>
                <td><span class="color-sample" style="background-color: #808080;"></span> Серый</td>
            </tr>
        </table>
    </div>
    
    <!-- Additional content would continue here -->
    
</body>
</html>
"""

def show_help_page():
    """
    Отображает страницу помощи/документации в интерфейсе Streamlit
    """
    st.title("📚 Руководство пользователя")
    st.header("🧮 Система прогнозирования сверхнормативных запасов (СНЗ и КСНЗ)")
    
    # Оглавление в сайдбаре
    with st.sidebar:
        st.markdown("### 📑 Содержание")
        toc_selection = st.radio(
            "Перейти к разделу:",
            ["Общее описание системы", 
             "Методы прогнозирования", 
             "Подготовка данных", 
             "Работа с приложением", 
             "Интерпретация результатов", 
             "Особые случаи и обработка исключений", 
             "Формулы и алгоритмы расчета"],
            label_visibility="collapsed"
        )
    
    # Отображаем содержимое документации
    st.markdown(get_documentation_content(), unsafe_allow_html=True)