import tabula
import pandas as pd

tabula.convert_into(r'Tarea 1\lista_precios.pdf',
                    r'Tarea 1\lista_precios.csv',
                    pages="all",
                    output_format="csv")

df = pd.read_csv(r'Tarea 1\lista_precios.csv')
df = df.drop(10, axis=0)
d_names = df.set_index('PRODUCTOS').to_dict()

lista_precios_float = []
lista_productos = []
for value in d_names["PRECIOS"]:
    # print(d_names["PRECIOS"][value].replace("$", ""))  # Trae los precios
    lista_precios_float.append(
        float(d_names["PRECIOS"][value].replace("$", "").replace(",", ".")))

# for elem in lista_precios_float:
#     print(elem)

for value in d_names['PRECIOS']:
    lista_productos.append(value)


d = dict(zip(lista_productos, lista_precios_float))


for key, value in d.items():
    print(key, value)
