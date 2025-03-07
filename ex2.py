import pandas as pd
import datetime
import os
from utils import generate_sample_data_method2

# Генерация тестовых данных для Метода 2
df_method2 = generate_sample_data_method2()

# Сохранение в Excel
if not os.path.exists('sample_data'):
    os.makedirs('sample_data')
    
df_method2.to_excel('sample_data/method2_sample.xlsx', index=False)
print("Файл сохранен: sample_data/method2_sample.xlsx")