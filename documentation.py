def get_documentation_content():
    """
    Возвращает содержимое документации по работе с приложением
    
    Returns:
        str: HTML-разметка с документацией
    """
    documentation = """
    <h1 style="color: #2B5797; text-align: center;">Руководство пользователя</h1>
    <h2 style="color: #2B5797;">Система прогнозирования сверхнормативных запасов (СНЗ и КСНЗ)</h2>
    
    <div style="margin-top: 20px;">
        <h3>Содержание</h3>
        <ol>
            <li><a href="#overview">Общее описание системы</a></li>
            <li><a href="#methods">Методы прогнозирования</a></li>
            <li><a href="#data-preparation">Подготовка данных</a></li>
            <li><a href="#usage">Работа с приложением</a></li>
            <li><a href="#results">Интерпретация результатов</a></li>
            <li><a href="#special-cases">Особые случаи и обработка исключений</a></li>
            <li><a href="#formulas">Формулы и алгоритмы расчета</a></li>
        </ol>
    </div>
    
    <div id="overview" style="margin-top: 40px;">
        <h3>1. Общее описание системы</h3>
        <p>
            Система прогнозирования сверхнормативных запасов (СНЗ и КСНЗ) предназначена для анализа и прогнозирования уровня складских запасов, 
            которые в будущем могут быть квалифицированы как критические (КСНЗ) или сверхнормативные (СНЗ).
        </p>
        <p>
            Система позволяет определить, когда конкретный материал перейдет в статус КСНЗ или СНЗ, если не будет использован, 
            что дает возможность заблаговременно принять меры по вовлечению материала в производство, предотвращая его переход в категорию неликвидов.
        </p>
        <p>
            <b>Основные термины:</b>
        </p>
        <ul>
            <li><b>Ликвидный запас</b> — запас, хранящийся на складе менее определенного периода (обычно до 9 месяцев для Метода 1 и до 10 месяцев для Метода 2).</li>
            <li><b>КСНЗ (Критический сверхнормативный запас)</b> — запас, который находится на грани перехода в сверхнормативный (обычно от 9-10 месяцев до 1 года).</li>
            <li><b>СНЗ (Сверхнормативный запас)</b> — запас, хранящийся на складе дольше допустимого срока (более 1 года до 3 лет).</li>
            <li><b>СНЗ > 3 лет</b> — запас, хранящийся на складе более 3 лет, который с высокой вероятностью требует списания.</li>
        </ul>
    </div>
    
    <div id="methods" style="margin-top: 40px;">
        <h3>2. Методы прогнозирования</h3>
        <p>
            В системе реализованы два метода прогнозирования:
        </p>
        
        <h4>Метод 1: Прогноз с учетом потребности</h4>
        <p>
            Этот метод использует данные о текущем запасе и прогнозируемой потребности для определения, 
            когда материалы перейдут в категорию КСНЗ или СНЗ, если потребление будет происходить согласно прогнозу.
        </p>
        <p>
            <b>Шкала старения для Метода 1:</b>
        </p>
        <table border="1" style="border-collapse: collapse; width: 100%;">
            <tr style="background-color: #f2f2f2;">
                <th style="padding: 8px; text-align: left;">Интервалы шкалы старения</th>
                <th style="padding: 8px; text-align: center;">Нижняя граница (дни)</th>
                <th style="padding: 8px; text-align: center;">Верхняя граница (дни)</th>
                <th style="padding: 8px; text-align: center;">Категория запаса</th>
            </tr>
            <tr>
                <td style="padding: 8px;">< 1 месяца</td>
                <td style="padding: 8px; text-align: center;">0</td>
                <td style="padding: 8px; text-align: center;">30</td>
                <td style="padding: 8px; text-align: center; background-color: #00b050; color: white;">Ликвидный</td>
            </tr>
            <tr>
                <td style="padding: 8px;">1-3 месяцев</td>
                <td style="padding: 8px; text-align: center;">31</td>
                <td style="padding: 8px; text-align: center;">91</td>
                <td style="padding: 8px; text-align: center; background-color: #00b050; color: white;">Ликвидный</td>
            </tr>
            <tr>
                <td style="padding: 8px;">3-6 месяцев</td>
                <td style="padding: 8px; text-align: center;">92</td>
                <td style="padding: 8px; text-align: center;">183</td>
                <td style="padding: 8px; text-align: center; background-color: #00b050; color: white;">Ликвидный</td>
            </tr>
            <tr>
                <td style="padding: 8px;">6-9 месяцев</td>
                <td style="padding: 8px; text-align: center;">184</td>
                <td style="padding: 8px; text-align: center;">274</td>
                <td style="padding: 8px; text-align: center; background-color: #00b050; color: white;">Ликвидный</td>
            </tr>
            <tr>
                <td style="padding: 8px;">9-12 месяцев</td>
                <td style="padding: 8px; text-align: center;">275</td>
                <td style="padding: 8px; text-align: center;">365</td>
                <td style="padding: 8px; text-align: center; background-color: #ffbf00;">КСНЗ</td>
            </tr>
            <tr>
                <td style="padding: 8px;">12-18 месяцев</td>
                <td style="padding: 8px; text-align: center;">366</td>
                <td style="padding: 8px; text-align: center;">548</td>
                <td style="padding: 8px; text-align: center; background-color: #ff4c4c; color: white;">СНЗ</td>
            </tr>
            <tr>
                <td style="padding: 8px;">18-24 месяца</td>
                <td style="padding: 8px; text-align: center;">549</td>
                <td style="padding: 8px; text-align: center;">730</td>
                <td style="padding: 8px; text-align: center; background-color: #ff4c4c; color: white;">СНЗ</td>
            </tr>
            <tr>
                <td style="padding: 8px;">2-3 года</td>
                <td style="padding: 8px; text-align: center;">731</td>
                <td style="padding: 8px; text-align: center;">1096</td>
                <td style="padding: 8px; text-align: center; background-color: #ff4c4c; color: white;">СНЗ</td>
            </tr>
            <tr>
                <td style="padding: 8px;">3-4 года</td>
                <td style="padding: 8px; text-align: center;">1097</td>
                <td style="padding: 8px; text-align: center;">1461</td>
                <td style="padding: 8px; text-align: center; background-color: #c00000; color: white;">СНЗ > 3 лет</td>
            </tr>
            <tr>
                <td style="padding: 8px;">4-5 лет</td>
                <td style="padding: 8px; text-align: center;">1462</td>
                <td style="padding: 8px; text-align: center;">1826</td>
                <td style="padding: 8px; text-align: center; background-color: #c00000; color: white;">СНЗ > 3 лет</td>
            </tr>
            <tr>
                <td style="padding: 8px;">>5 лет</td>
                <td style="padding: 8px; text-align: center;">1827</td>
                <td style="padding: 8px; text-align: center;">9999</td>
                <td style="padding: 8px; text-align: center; background-color: #c00000; color: white;">СНЗ > 3 лет</td>
            </tr>
        </table>
        
        <h4 style="margin-top: 20px;">Метод 2: Прогноз без учета потребности (только фактический запас)</h4>
        <p>
            Этот метод основан только на текущем фактическом запасе на складе, без учета потребности и планируемого обеспечения. 
            Он показывает, когда материалы перейдут в категорию КСНЗ или СНЗ, если не будут использованы вообще.
        </p>
        <p>
            <b>Шкала старения для Метода 2:</b>
        </p>
        <table border="1" style="border-collapse: collapse; width: 100%;">
            <tr style="background-color: #f2f2f2;">
                <th style="padding: 8px; text-align: left;">Интервалы шкалы старения</th>
                <th style="padding: 8px; text-align: center;">Нижняя граница (дни)</th>
                <th style="padding: 8px; text-align: center;">Верхняя граница (дни)</th>
                <th style="padding: 8px; text-align: center;">Категория запаса</th>
            </tr>
            <tr>
                <td style="padding: 8px;">< 1 месяца</td>
                <td style="padding: 8px; text-align: center;">0</td>
                <td style="padding: 8px; text-align: center;">29</td>
                <td style="padding: 8px; text-align: center; background-color: #00b050; color: white;">Ликвидный</td>
            </tr>
            <tr>
                <td style="padding: 8px;">1 месяц</td>
                <td style="padding: 8px; text-align: center;">30</td>
                <td style="padding: 8px; text-align: center;">59</td>
                <td style="padding: 8px; text-align: center; background-color: #00b050; color: white;">Ликвидный</td>
            </tr>
            <tr>
                <td style="padding: 8px;">2 месяца</td>
                <td style="padding: 8px; text-align: center;">60</td>
                <td style="padding: 8px; text-align: center;">90</td>
                <td style="padding: 8px; text-align: center; background-color: #00b050; color: white;">Ликвидный</td>
            </tr>
            <tr>
                <td style="padding: 8px;">3 месяца</td>
                <td style="padding: 8px; text-align: center;">91</td>
                <td style="padding: 8px; text-align: center;">121</td>
                <td style="padding: 8px; text-align: center; background-color: #00b050; color: white;">Ликвидный</td>
            </tr>
            <tr>
                <td style="padding: 8px;">4 месяца</td>
                <td style="padding: 8px; text-align: center;">122</td>
                <td style="padding: 8px; text-align: center;">152</td>
                <td style="padding: 8px; text-align: center; background-color: #00b050; color: white;">Ликвидный</td>
            </tr>
            <tr>
                <td style="padding: 8px;">5 месяцев</td>
                <td style="padding: 8px; text-align: center;">153</td>
                <td style="padding: 8px; text-align: center;">182</td>
                <td style="padding: 8px; text-align: center; background-color: #00b050; color: white;">Ликвидный</td>
            </tr>
            <tr>
                <td style="padding: 8px;">6 месяцев</td>
                <td style="padding: 8px; text-align: center;">183</td>
                <td style="padding: 8px; text-align: center;">213</td>
                <td style="padding: 8px; text-align: center; background-color: #00b050; color: white;">Ликвидный</td>
            </tr>
            <tr>
                <td style="padding: 8px;">7 месяцев</td>
                <td style="padding: 8px; text-align: center;">214</td>
                <td style="padding: 8px; text-align: center;">244</td>
                <td style="padding: 8px; text-align: center; background-color: #00b050; color: white;">Ликвидный</td>
            </tr>
            <tr>
                <td style="padding: 8px;">8 месяцев</td>
                <td style="padding: 8px; text-align: center;">245</td>
                <td style="padding: 8px; text-align: center;">273</td>
                <td style="padding: 8px; text-align: center; background-color: #00b050; color: white;">Ликвидный</td>
            </tr>
            <tr>
                <td style="padding: 8px;">9 месяцев</td>
                <td style="padding: 8px; text-align: center;">274</td>
                <td style="padding: 8px; text-align: center;">304</td>
                <td style="padding: 8px; text-align: center; background-color: #00b050; color: white;">Ликвидный</td>
            </tr>
            <tr>
                <td style="padding: 8px;">10 месяцев</td>
                <td style="padding: 8px; text-align: center;">305</td>
                <td style="padding: 8px; text-align: center;">334</td>
                <td style="padding: 8px; text-align: center; background-color: #ffbf00;">КСНЗ</td>
            </tr>
            <tr>
                <td style="padding: 8px;">11 месяцев</td>
                <td style="padding: 8px; text-align: center;">335</td>
                <td style="padding: 8px; text-align: center;">364</td>
                <td style="padding: 8px; text-align: center; background-color: #ffbf00;">КСНЗ</td>
            </tr>
            <tr>
                <td style="padding: 8px;">12-18 месяцев</td>
                <td style="padding: 8px; text-align: center;">365</td>
                <td style="padding: 8px; text-align: center;">547</td>
                <td style="padding: 8px; text-align: center; background-color: #ff4c4c; color: white;">СНЗ</td>
            </tr>
            <tr>
                <td style="padding: 8px;">18-24 месяца</td>
                <td style="padding: 8px; text-align: center;">548</td>
                <td style="padding: 8px; text-align: center;">1095</td>
                <td style="padding: 8px; text-align: center; background-color: #ff4c4c; color: white;">СНЗ</td>
            </tr>
            <tr>
                <td style="padding: 8px;">> 3 лет</td>
                <td style="padding: 8px; text-align: center;">1096</td>
                <td style="padding: 8px; text-align: center;">9999</td>
                <td style="padding: 8px; text-align: center; background-color: #c00000; color: white;">СНЗ > 3 лет</td>
            </tr>
            <tr>
                <td style="padding: 8px;">Без даты в SAP ERP</td>
                <td style="padding: 8px; text-align: center;">≥ 10000</td>
                <td style="padding: 8px; text-align: center;">-</td>
                <td style="padding: 8px; text-align: center; background-color: #808080; color: white;">Требует проверки</td>
            </tr>
        </table>
    </div>
    
    <div id="data-preparation" style="margin-top: 40px;">
        <h3>3. Подготовка данных</h3>
        <p>
            Для работы с системой прогнозирования требуется подготовить исходные данные в формате Excel или CSV. 
            Требования к данным различаются в зависимости от выбранного метода прогнозирования.
        </p>
        
        <h4>Для Метода 1: Прогноз с учетом потребности</h4>
        <p>
            Необходимый формат данных (отчет ZMML_REP_RD):
        </p>
        <table border="1" style="border-collapse: collapse; width: 100%;">
            <tr style="background-color: #f2f2f2;">
                <th style="padding: 8px; text-align: left;">Колонка</th>
                <th style="padding: 8px; text-align: left;">Описание</th>
                <th style="padding: 8px; text-align: left;">Обязательность</th>
            </tr>
            <tr>
                <td style="padding: 8px;">БЕ</td>
                <td style="padding: 8px;">Бизнес-единица</td>
                <td style="padding: 8px;">Обязательно</td>
            </tr>
            <tr>
                <td style="padding: 8px;">Область планирования</td>
                <td style="padding: 8px;">Область планирования</td>
                <td style="padding: 8px;">Обязательно</td>
            </tr>
            <tr>
                <td style="padding: 8px;">Материал</td>
                <td style="padding: 8px;">Код материала</td>
                <td style="padding: 8px;">Обязательно</td>
            </tr>
            <tr>
                <td style="padding: 8px;">Количество обеспечения</td>
                <td style="padding: 8px;">Текущее количество на складе</td>
                <td style="padding: 8px;">Обязательно</td>
            </tr>
            <tr>
                <td style="padding: 8px;">Дата поступления</td>
                <td style="padding: 8px;">Историческая дата поступления или дата поступления на склад</td>
                <td style="padding: 8px;">Обязательно</td>
            </tr>
            <tr>
                <td style="padding: 8px;">Дневное потребление</td>
                <td style="padding: 8px;">Среднее дневное потребление материала</td>
                <td style="padding: 8px;">Опционально (если не указано, будет считаться равным 0)</td>
            </tr>
        </table>
        
        <h4 style="margin-top: 20px;">Для Метода 2: Прогноз без учета потребности</h4>
        <p>
            Необходимый формат данных (отчет MB52):
        </p>
        <table border="1" style="border-collapse: collapse; width: 100%;">
            <tr style="background-color: #f2f2f2;">
                <th style="padding: 8px; text-align: left;">Колонка</th>
                <th style="padding: 8px; text-align: left;">Описание</th>
                <th style="padding: 8px; text-align: left;">Обязательность</th>
            </tr>
            <tr>
                <td style="padding: 8px;">БЕ</td>
                <td style="padding: 8px;">Бизнес-единица</td>
                <td style="padding: 8px;">Обязательно</td>
            </tr>
            <tr>
                <td style="padding: 8px;">Завод</td>
                <td style="padding: 8px;">Код завода</td>
                <td style="padding: 8px;">Обязательно</td>
            </tr>
            <tr>
                <td style="padding: 8px;">Склад</td>
                <td style="padding: 8px;">Код склада</td>
                <td style="padding: 8px;">Обязательно</td>
            </tr>
            <tr>
                <td style="padding: 8px;">Материал</td>
                <td style="padding: 8px;">Код материала</td>
                <td style="padding: 8px;">Обязательно</td>
            </tr>
            <tr>
                <td style="padding: 8px;">Партия</td>
                <td style="padding: 8px;">Номер партии</td>
                <td style="padding: 8px;">Обязательно</td>
            </tr>
            <tr>
                <td style="padding: 8px;">СПП элемент</td>
                <td style="padding: 8px;">СПП элемент</td>
                <td style="padding: 8px;">Обязательно (может быть пустым)</td>
            </tr>
            <tr>
                <td style="padding: 8px;">Дата поступления на склад</td>
                <td style="padding: 8px;">Дата поступления материала на склад</td>
                <td style="padding: 8px;">Обязательно</td>
            </tr>
            <tr>
                <td style="padding: 8px;">Фактический запас</td>
                <td style="padding: 8px;">Текущее количество на складе</td>
                <td style="padding: 8px;">Обязательно</td>
            </tr>
        </table>
        
        <p style="margin-top: 20px;">
            <b>Важно:</b> Даты в исходных данных должны быть в формате, который может быть распознан как дата (например, YYYY-MM-DD, DD.MM.YYYY).
            Числовые данные (количество, потребление) должны быть представлены в виде чисел, а не текста.
        </p>
        
        <p>
            Вы можете скачать примеры шаблонов данных для обоих методов с помощью кнопок в боковой панели приложения.
        </p>
    </div>
    
    <div id="usage" style="margin-top: 40px;">
        <h3>4. Работа с приложением</h3>
        <p>
            Для работы с системой прогнозирования СНЗ и КСНЗ выполните следующие шаги:
        </p>
        
        <h4>Шаг 1: Выбор метода прогнозирования</h4>
        <p>
            В боковой панели выберите один из двух методов прогнозирования:
        </p>
        <ul>
            <li><b>Метод 1: С учетом потребности</b> — Если вы хотите учитывать прогнозное потребление материалов.</li>
            <li><b>Метод 2: Без учета потребности</b> — Если вы хотите проанализировать только фактический запас.</li>
        </ul>
        
        <h4>Шаг 2: Загрузка данных</h4>
        <p>
            Выберите источник данных:
        </p>
        <ul>
            <li><b>Загрузить Excel файл</b> — Загрузите подготовленный файл с данными в формате Excel (.xlsx, .xls).</li>
            <li><b>Использовать тестовые данные</b> — Используйте тестовые данные, предоставляемые системой для демонстрации работы.</li>
        </ul>
        
        <h4>Шаг 3: Настройка параметров прогнозирования</h4>
        <p>
            Укажите дополнительные параметры:
        </p>
        <ul>
            <li><b>Дата окончания прогноза</b> — До какой даты в будущем нужно построить прогноз (до 5 лет от текущей даты).</li>
            <li><b>Шаг прогноза (дни)</b> — С каким интервалом строить прогноз (по умолчанию 30 дней).</li>
        </ul>
        
        <h4>Шаг 4: Запуск прогнозирования</h4>
        <p>
            Нажмите кнопку <b>"Рассчитать прогноз"</b> для запуска процесса прогнозирования.
            Система проанализирует данные и отобразит результаты.
        </p>
        
        <h4>Шаг 5: Анализ результатов</h4>
        <p>
            Результаты прогнозирования отображаются в трех вкладках:
        </p>
        <ul>
            <li><b>Динамика запасов</b> — Графики изменения объемов запасов по категориям с течением времени.</li>
            <li><b>Таблица сводных результатов</b> — Сводные данные по категориям запасов на каждую дату прогноза.</li>
            <li><b>Детальные результаты</b> — Подробная информация по каждому материалу на выбранную дату прогноза.</li>
        </ul>
        
        <h4>Шаг 6: Экспорт результатов</h4>
        <p>
            Вы можете экспортировать результаты прогнозирования в Excel, выбрав один из форматов:
        </p>
        <ul>
            <li><b>Excel (все данные)</b> — Экспорт всех данных, включая детальные результаты по каждой дате.</li>
            <li><b>Excel (только сводные данные)</b> — Экспорт только сводных результатов без детализации.</li>
        </ul>
    </div>
    
    <div id="results" style="margin-top: 40px;">
        <h3>5. Интерпретация результатов</h3>
        <p>
            Результаты прогнозирования представлены в различных форматах для удобства анализа:
        </p>
        
        <h4>Графики динамики запасов</h4>
        <p>
            <b>Линейный график</b> показывает изменение объема запасов по категориям на протяжении всего периода прогнозирования.
            Это позволяет увидеть тренды и моменты, когда происходит существенное изменение структуры запасов.
        </p>
        <p>
            <b>График-область</b> отображает структуру запасов в процентном соотношении по категориям.
            Он позволяет оценить пропорции между различными категориями запасов в каждый момент времени.
        </p>
        <p>
            Графики используют следующую цветовую кодировку:
        </p>
        <ul>
            <li><span style="display: inline-block; width: 20px; height: 20px; background-color: #00b050; vertical-align: middle;"></span> <b>Зеленый</b> — Ликвидный запас</li>
            <li><span style="display: inline-block; width: 20px; height: 20px; background-color: #ffbf00; vertical-align: middle;"></span> <b>Желтый</b> — КСНЗ (Критический сверхнормативный запас)</li>
            <li><span style="display: inline-block; width: 20px; height: 20px; background-color: #ff4c4c; vertical-align: middle;"></span> <b>Светло-красный</b> — СНЗ (Сверхнормативный запас)</li>
            <li><span style="display: inline-block; width: 20px; height: 20px; background-color: #c00000; vertical-align: middle;"></span> <b>Темно-красный</b> — СНЗ > 3 лет</li>
            <li><span style="display: inline-block; width: 20px; height: 20px; background-color: #808080; vertical-align: middle;"></span> <b>Серый</b> — Требует проверки (для материалов без даты)</li>
        </ul>
        
        <h4>Таблица сводных результатов</h4>
        <p>
            Таблица содержит агрегированные данные по каждой категории запасов на каждую дату прогноза:
        </p>
        <ul>
            <li><b>Дата прогноза</b> — Дата, на которую построен прогноз.</li>
            <li><b>Категория</b> — Категория запаса (Ликвидный, КСНЗ, СНЗ, СНЗ > 3 лет).</li>
            <li><b>Количество</b> — Суммарное количество запасов в данной категории.</li>
        </ul>
        <p>
            Эта таблица позволяет быстро оценить динамику изменения объемов запасов по категориям и выявить моменты, 
            когда происходит существенное увеличение КСНЗ или СНЗ.
        </p>
        
        <h4>Детальные результаты</h4>
        <p>
            Таблица детальных результатов позволяет анализировать прогноз на уровне отдельных материалов:
        </p>
        <ul>
            <li>В этой таблице отображаются все материалы из исходных данных.</li>
            <li>Для каждого материала указана категория запаса на выбранную дату прогноза.</li>
            <li>При прогнозировании по Методу 1 также указывается оставшееся количество с учетом потребления.</li>
            <li>Материалы, которые в выбранную дату будут относиться к КСНЗ или СНЗ, выделены соответствующими цветами.</li>
        </ul>
        <p>
            Фильтр по дате прогноза позволяет просматривать состояние запасов на любую дату в пределах периода прогнозирования.
        </p>
    </div>
    
    <div id="special-cases" style="margin-top: 40px;">
        <h3>6. Особые случаи и обработка исключений</h3>
        <p>
            Система предусматривает обработку различных особых случаев и исключений, которые могут возникнуть при работе с данными:
        </p>
        
        <h4>Партии с разными датами поступления</h4>
        <p>
            В некоторых случаях одна и та же партия материала может иметь несколько записей с разными датами поступления.
            Например, часть партии могла быть принята на склад в один день, а другая часть — в другой.
        </p>
        <p>
            <b>Обработка:</b> Система анализирует такие случаи и обрабатывает их следующим образом:
        </p>
        <ul>
            <li>Если все записи партии относятся к одной категории запаса, они объединяются в одну запись с суммарным количеством.</li>
            <li>Если записи партии относятся к разным категориям (например, часть партии — ликвидный запас, а часть — КСНЗ), 
                система создает отдельные записи для каждой категории с соответствующим количеством.</li>
        </ul>
        <p>
            Пример:
        </p>
        <table border="1" style="border-collapse: collapse; width: 100%;">
            <tr style="background-color: #f2f2f2;">
                <th style="padding: 8px; text-align: left;">БЕ</th>
                <th style="padding: 8px; text-align: left;">Завод</th>
                <th style="padding: 8px; text-align: left;">Склад</th>
                <th style="padding: 8px; text-align: left;">Материал</th>
                <th style="padding: 8px; text-align: left;">Партия</th>
                <th style="padding: 8px; text-align: left;">Дата поступления</th>
                <th style="padding: 8px; text-align: left;">Количество</th>
                <th style="padding: 8px; text-align: left;">Категория</th>
            </tr>
            <tr>
                <td style="padding: 8px;">0101</td>
                <td style="padding: 8px;">1111</td>
                <td style="padding: 8px;">1111</td>
                <td style="padding: 8px;">222222</td>
                <td style="padding: 8px;">1111222444</td>
                <td style="padding: 8px;">27.12.2023</td>
                <td style="padding: 8px;">30</td>
                <td style="padding: 8px;">КСНЗ</td>
            </tr>
            <tr>
                <td style="padding: 8px;">0101</td>
                <td style="padding: 8px;">1111</td>
                <td style="padding: 8px;">1111</td>
                <td style="padding: 8px;">222222</td>
                <td style="padding: 8px;">1111222444</td>
                <td style="padding: 8px;">10.01.2024</td>
                <td style="padding: 8px;">70</td>
                <td style="padding: 8px;">Ликвидный</td>
            </tr>
        </table>
        <p>
            В этом примере часть партии поступила в декабре 2023 года (30 единиц), а часть — в январе 2024 года (70 единиц).
            При прогнозировании система будет учитывать разные даты поступления и соответствующие категории запаса.
        </p>
        
        <h4>Материалы без даты поступления</h4>
        <p>
            В некоторых случаях в данных может отсутствовать информация о дате поступления материала на склад.
        </p>
        <p>
            <b>Обработка:</b> Материалы без даты поступления помечаются специальной категорией "Требует проверки" 
            и выделяются серым цветом в результатах. Такие материалы требуют дополнительного анализа и уточнения данных.
        </p>
        
        <h4>Отсутствие данных о потреблении</h4>
        <p>
            При использовании Метода 1 (с учетом потребности) может отсутствовать информация о дневном потреблении материалов.
        </p>
        <p>
            <b>Обработка:</b> Если колонка "Дневное потребление" отсутствует в исходных данных, система автоматически
            добавляет ее и заполняет нулевыми значениями. В этом случае прогноз будет строиться исходя из предположения,
            что материалы не потребляются (аналогично Методу 2).
        </p>
    </div>
    
    <div id="formulas" style="margin-top: 40px;">
        <h3>7. Формулы и алгоритмы расчета</h3>
        <p>
            В основе прогнозирования лежат следующие формулы и алгоритмы:
        </p>
        
        <h4>Расчет количества дней хранения</h4>
        <pre style="background-color: #f5f5f5; padding: 10px; border-radius: 5px;">
Дни хранения = Дата прогноза - Дата поступления
        </pre>
        <p>
            Этот расчет выполняется для каждого материала на каждую дату прогноза.
            В результате определяется, сколько дней будет храниться материал к указанной дате прогноза.
        </p>
        
        <h4>Определение категории запаса (Метод 1)</h4>
        <pre style="background-color: #f5f5f5; padding: 10px; border-radius: 5px;">
Если Дни хранения < 275:
    Категория = "Ликвидный"
Иначе если Дни хранения < 366:
    Категория = "КСНЗ"
Иначе если Дни хранения < 1097:
    Категория = "СНЗ"
Иначе:
    Категория = "СНЗ > 3 лет"
        </pre>
        
        <h4>Определение категории запаса (Метод 2)</h4>
        <pre style="background-color: #f5f5f5; padding: 10px; border-radius: 5px;">
Если Дни хранения < 305:
    Категория = "Ликвидный"
Иначе если Дни хранения < 365:
    Категория = "КСНЗ"
Иначе если Дни хранения < 1096:
    Категория = "СНЗ"
Иначе:
    Категория = "СНЗ > 3 лет"
        </pre>
        
        <h4>Расчет оставшегося количества с учетом потребления (для Метода 1)</h4>
        <pre style="background-color: #f5f5f5; padding: 10px; border-radius: 5px;">
Дни от текущей даты = Дата прогноза - Текущая дата
Оставшееся количество = Количество обеспечения - (Дневное потребление * Дни от текущей даты)
Если Оставшееся количество < 0:
    Оставшееся количество = 0
        </pre>
        <p>
            Этот расчет позволяет учесть потребление материала при прогнозировании. 
            Если материал полностью израсходуется до даты прогноза, его оставшееся количество будет равно 0,
            и он не будет учитываться в статистике КСНЗ/СНЗ.
        </p>
        
        <h4>Алгоритм прогнозирования</h4>
        <p>
            Общий алгоритм прогнозирования включает следующие шаги:
        </p>
        <ol>
            <li>Определение дат прогноза с заданным шагом от текущей даты до указанной даты окончания прогноза.</li>
            <li>Для каждой даты прогноза:
                <ul>
                    <li>Расчет количества дней хранения для каждого материала.</li>
                    <li>Для Метода 1: Расчет оставшегося количества с учетом потребления.</li>
                    <li>Определение категории запаса для каждого материала.</li>
                    <li>Агрегация данных по категориям (суммирование количества).</li>
                </ul>
            </li>
            <li>Формирование сводных и детальных результатов в виде графиков и таблиц.</li>
        </ol>
    </div>
    """
    return documentation