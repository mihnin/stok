import pandas as pd
import datetime
import os
from utils import generate_sample_data_method1

# Генерация тестовых данных для Метода 1
df_method1 = generate_sample_data_method1()

# Сохранение в Excel
if not os.path.exists('sample_data'):
    os.makedirs('sample_data')
    
df_method1.to_excel('sample_data/method1_sample.xlsx', index=False)
print("Файл сохранен: sample_data/method1_sample.xlsx")