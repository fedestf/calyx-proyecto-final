import tabula
import pandas as pd
from funciones import pdf_to_csv, dict_from_csv

pdf_to_csv(a_convertir=r'Tarea 1\lista_precios.pdf',
           destino=r'Tarea 1\lista_precios.csv',
           paginas="all")

dict_from_csv(csv=r'Tarea 1\lista_precios.csv')


for key, value in dict_from_csv(csv=r'Tarea 1\lista_precios.csv').items():
    print(key, value)
