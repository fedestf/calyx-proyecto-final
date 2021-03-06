import tabula
import pandas as pd
import xml.etree.ElementTree as ET
import glob
import json
import pyautogui
from datetime import date
import time
from loggers import logger_debug, logger_error
# agrego un valor a la lista para poder borrarlo y que tome el primer nombre como posicion 0
nombre = [1]


def splitter(archivo):

    try:
        # borro la posicion anterior de la lista para que me tome el archivo que sigue
        nombre.pop()
        # traigo lo que haya despues de la ultima barra en la direccion
        nombre.append(archivo[24::1])
        # reemplazo el .txt por un espacio iterando asi para poder usar el metodo replace de string
        # str(i) para que no tire el error que la instancia int de i no tiene el metodo replace
        nombre_limpio = [str(i).replace(".txt", "")for i in nombre]

        for nombre_archivo in nombre_limpio:
            return nombre_archivo

        logger_debug.debug("Funcion ejecutada con exito")

    except Exception as e:
        logger_error.error(e)


def pdf_to_csv(a_convertir, destino, paginas):
    tabula.convert_into(a_convertir,
                        destino,
                        pages=paginas,
                        output_format="csv")


def dict_from_csv(csv):
    df = pd.read_csv(csv)
    df = df.drop(10, axis=0)
    dic_nombre = df.set_index('PRODUCTOS').to_dict()

    lista_precios_float = []
    lista_productos = []
    for value in dic_nombre["PRECIOS"]:

        lista_precios_float.append(
            float(dic_nombre["PRECIOS"][value].replace("$", "").replace(",", ".")))

    for value in dic_nombre['PRECIOS']:
        lista_productos.append(value)

    lista_precios = dict(zip(lista_productos, lista_precios_float))

    return lista_precios


def validacion_facturas_y_json_a_cargar(carpeta_facturas):

    lista_facturas_xml = glob.glob(carpeta_facturas)

    lista_facturas = []

    facturas = {}

    for factura in lista_facturas_xml:

        tree = ET.parse(factura)

        root = tree.getroot()

        namespace = {
            'cac': "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
            'cbc': "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",

        }

        id_factura = root.find('cbc:ID', namespace)
        fecha = root.find('cbc:IssueDate', namespace)

        lista_facturas.append(f'{id_factura.text}')
        facturas[f'{id_factura.text}'] = []

        for x in root.findall('cac:InvoiceLine', namespace):

            for item in x.findall('cac:Item', namespace):

                nombre = item.find('cbc:Description', namespace)

                for seller_id in item.findall('cac:SellersItemIdentification', namespace):
                    id_seller = seller_id.find('cbc:ID', namespace)

            for valor in x.findall('cac:Price', namespace):

                valor_item = valor.find('cbc:UnitPrice', namespace)
                cantidad_item = valor.find('cbc:BaseQuantity', namespace)

                valor = float(valor_item.text)
                cantidad = float(cantidad_item.text)

            subtotal = valor*cantidad
            facturas[f'{id_factura.text}'].append({'fecha': fecha.text,
                                                   'id_seller': id_seller.text,
                                                   'nombre': nombre.text,
                                                   'valor': valor,
                                                   'cantidad': cantidad,
                                                   'subtotal': subtotal})

            with open(r'Tarea 1\facturas.json', 'w') as file:
                json.dump(facturas, file, indent=4)

    dic_facturas = {}
    with open(r'Tarea 1\facturas.json') as data_file:
        dic_facturas = json.load(data_file)

    lista_bool_nombre = []
    lista_bool_valor = []
    facturas_carga = {}
    facturas_erroneas = []

    for factura in lista_facturas:

        facturas_carga[f'{factura}'] = []

        for key, value in dic_facturas.items():

            if factura == key:
                for key in dic_facturas[f'{factura}']:
                    # print(factura, key['nombre'], key['valor'])
                    if key['nombre'] in [keyd for keyd in dict_from_csv(csv=r'Tarea 1\lista_precios.csv').keys()]:
                        lista_bool_nombre.append(True)

                        if key['valor'] in [keyv for keyv in dict_from_csv(csv=r'Tarea 1\lista_precios.csv').values()]:

                            subtotal_verificador = key['valor']*key['cantidad']

                            if key['subtotal'] == subtotal_verificador:
                                lista_bool_valor.append(True)

                if len(lista_bool_nombre) == len(lista_bool_valor):

                    print(f"valores ok en la factura {factura}")

                    for key in dic_facturas[f'{factura}']:

                        facturas_carga[f'{factura}'].append({'fecha': key['fecha'],
                                                             'id_seller': key['id_seller'],
                                                             'nombre': key['nombre'],
                                                             'valor': key['valor'],
                                                             'cantidad': key['cantidad'],
                                                             'subtotal': subtotal},)
                else:
                    print(f"valores erroneos en la factura {factura}")
                    facturas_erroneas.append(factura)
                with open(r'Tarea 1\facturas_a_cargar.json', 'w') as file:
                    json.dump(facturas_carga, file, indent=4)
                lista_bool_valor.clear()
                lista_bool_nombre.clear()


def carga_id_y_fecha(id_factura, dia, mes, año):
    try:
        time.sleep(4)
        coords_icono = pyautogui.locateCenterOnScreen(
            r'Tarea 1\sistema.png', confidence=0.9)
        time.sleep(2)

        pyautogui.click(*coords_icono, clicks=2)
        time.sleep(2)

        coords_id_factura = pyautogui.locateCenterOnScreen(
            r'Tarea 1\id_factura.png')

        pyautogui.click(*coords_id_factura, clicks=1)
        pyautogui.typewrite(id_factura, interval=1)
        pyautogui.press("tab")

        dia_factura = int(dia)
        fecha_hoy = date.today().strftime("%d-%m-%Y")
        dia_hoy = int(fecha_hoy[0:2:1])

        if dia_factura == dia_hoy:

            time.sleep(0.5)
            pyautogui.press("left")

        if dia_factura < dia_hoy:

            while dia_factura != dia_hoy:

                dia_hoy = dia_hoy-1
                time.sleep(0.5)
                pyautogui.press("down")

            time.sleep(0.5)
            pyautogui.press("right")

        if dia_factura > dia_hoy:

            while dia_factura != dia_hoy:

                dia_hoy = dia_hoy+1
                time.sleep(0.5)
                pyautogui.press("up")

            time.sleep(0.5)
            pyautogui.press("right")

        mes_factura = int(mes)
        fecha_hoy = date.today().strftime("%d-%m-%Y")
        mes_hoy = int(fecha_hoy[3:5:1])

        if mes_factura == mes_hoy:

            time.sleep(0.5)
            pyautogui.press("left")

        if mes_factura < mes_hoy:

            while mes_factura != mes_hoy:

                mes_hoy = mes_hoy-1

                time.sleep(0.5)
                pyautogui.press("down")

            time.sleep(0.5)
            pyautogui.press("right")

        if mes_factura > mes_hoy:

            while mes_factura != mes_hoy:

                mes_hoy = mes_hoy+1

                time.sleep(0.5)
                pyautogui.press("up")

            time.sleep(0.5)
            pyautogui.press("right")

        año_factura = int(año)
        año_hoy = date.today().strftime("%d-%m-%Y")
        año_hoy = int(fecha_hoy[6::1])

        if año_factura == año_hoy:

            time.sleep(0.5)
            coords_agregar_item = pyautogui.locateCenterOnScreen(
                r'Tarea 1\agregar_item.png')
            pyautogui.click(*coords_agregar_item, clicks=1)

            coords_0_fondo_azul = pyautogui.locateCenterOnScreen(
                r'Tarea 1\0_fondo_azul.png')
            time.sleep(2)
            pyautogui.click(*coords_0_fondo_azul, clicks=1)
            time.sleep(2)

        if año_factura < año_hoy:

            while año_factura != año_hoy:

                año_hoy = año_hoy-1

                time.sleep(0.5)
                pyautogui.press("down")

            time.sleep(0.5)
            coords_agregar_item = pyautogui.locateCenterOnScreen(
                r'Tarea 1\agregar_item.png')
            pyautogui.click(*coords_agregar_item, clicks=1)

            coords_0_fondo_azul = pyautogui.locateCenterOnScreen(
                r'Tarea 1\0_fondo_azul.png')
            time.sleep(2)
            pyautogui.click(*coords_0_fondo_azul, clicks=1)
            time.sleep(2)

        if año_factura > año_hoy:

            while año_factura != año_hoy:

                año_hoy = año_hoy+1

                time.sleep(0.5)
                pyautogui.press("up")

            time.sleep(0.5)
            coords_agregar_item = pyautogui.locateCenterOnScreen(
                r'Tarea 1\agregar_item.png')
            pyautogui.click(*coords_agregar_item, clicks=1)

            coords_0_fondo_azul = pyautogui.locateCenterOnScreen(
                r'Tarea 1\0_fondo_azul.png')
            time.sleep(2)
            pyautogui.click(*coords_0_fondo_azul, clicks=1)
            time.sleep(2)

    except Exception as e:
        print(e)


def carga_productos(id_producto, nombre, valor, cantidad, subtotal):
    try:

        pyautogui.typewrite(id_producto, interval=0.5)

        time.sleep(1)
        pyautogui.press("tab")

        time.sleep(1)
        pyautogui.typewrite(nombre, interval=0.5)

        time.sleep(1)
        pyautogui.press("tab")

        time.sleep(1)
        pyautogui.typewrite(valor, interval=0.5)

        time.sleep(1)
        pyautogui.press("tab")

        time.sleep(1)
        pyautogui.typewrite(cantidad, interval=0.5)

        time.sleep(1)
        pyautogui.press("tab")

        time.sleep(1)
        pyautogui.typewrite(subtotal, interval=0.5)

        time.sleep(1)

    except Exception as e:
        print(e)
