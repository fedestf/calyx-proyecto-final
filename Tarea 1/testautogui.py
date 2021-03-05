import json
import pyautogui

dic_facturas_a_cargar = {}
with open(r'Tarea 1\facturas_a_cargar.json') as data_file:
    dic_facturas_a_cargar = json.load(data_file)


for key, value in dic_facturas_a_cargar.items():

    if value != []:
        id = key
        fecha = [value['fecha'] for value in dic_facturas_a_cargar[f'{id}']]
        dia = str(fecha[0])[8::1]
        mes = str(fecha[0])[5:7:1]
        año = str(fecha[0])[0:4:1]
        print(key, dia, mes, año)

        for value in dic_facturas_a_cargar[f'{id}']:

            id_seller = value['id_seller']
            nombre = value['nombre']
            valor = int(value['valor'])
            cantidad = str(value['cantidad']).replace('.', ',')
            subtotal = int(value['subtotal'])

            print(id_seller, nombre, valor, cantidad, subtotal)


# coords = pyautogui.locateCenterOnScreen(r'Tarea 1\sistema.png')

# pyautogui.click(*coords, clicks=2)
