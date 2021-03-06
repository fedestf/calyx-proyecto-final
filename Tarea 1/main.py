import xml.etree.ElementTree as ET
import os
import glob
import json
import pyautogui
from datetime import date
import time
import scrapper
from funciones import splitter, pdf_to_csv, dict_from_csv, validacion_facturas_y_json_a_cargar, carga_id_y_fecha, carga_productos
import scrapper
import smtplib
import ssl
from settings import PASSWORD, MAIL, DESTINATARIOS
from loggers import logger_debug, logger_error
from email.message import EmailMessage


pdf_to_csv(a_convertir=r'Tarea 1\lista_precios.pdf',
           destino=r'Tarea 1\lista_precios.csv',
           paginas="all")

dict_from_csv(csv=r'Tarea 1\lista_precios.csv')

ruta = r'Tarea 1\Facturas\*.xml'
lista_facturas_xml = glob.glob(ruta)

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
                                                         'subtotal': key['subtotal']},)
            else:
                print(f"valores erroneos en la factura {factura}")
                facturas_erroneas.append(factura)
            with open(r'Tarea 1\facturas_a_cargar.json', 'w') as file:
                json.dump(facturas_carga, file, indent=4)
            lista_bool_valor.clear()
            lista_bool_nombre.clear()

dic_facturas_a_cargar = {}
with open(r'Tarea 1\facturas_a_cargar.json') as data_file:
    dic_facturas_a_cargar = json.load(data_file)


for key, value in dic_facturas_a_cargar.items():

    if value != []:
        id = key

        fecha_factura = [value['fecha']
                         for value in dic_facturas_a_cargar[f'{id}']]
        dia_factura = str(fecha_factura[0])[8::1]
        mes_factura = str(fecha_factura[0])[5:7:1]
        año_factura = str(fecha_factura[0])[0:4:1]
        #
        carga_id_y_fecha(id_factura=key, dia=dia_factura,
                         mes=mes_factura, año=año_factura)

        for value in dic_facturas_a_cargar[f'{id}']:

            id_seller = value['id_seller']
            nombre = value['nombre']
            valor = int(value['valor'])
            cantidad = str(value['cantidad']).replace('.', ',')
            subtotal = int(value['subtotal'])

            carga_productos(id_seller, nombre, str(
                valor), cantidad, str(subtotal))

            coords_agregar_item = pyautogui.locateCenterOnScreen(
                r'Tarea 1\screenshots\agregar_item.png')
            time.sleep(1)
            pyautogui.click(*coords_agregar_item, clicks=1)
            time.sleep(1)
            coords_0_fondo_blanco = pyautogui.locateCenterOnScreen(
                r'Tarea 1\screenshots\0_fondo_blanco.png')
            pyautogui.click(*coords_0_fondo_blanco, clicks=1)
            time.sleep(1)

        coords_quitar_item = pyautogui.locateCenterOnScreen(
            r'Tarea 1\screenshots\quitar_item.png')
        time.sleep(1)
        pyautogui.click(*coords_quitar_item, clicks=1)
        time.sleep(1)
        coords_guardar = pyautogui.locateCenterOnScreen(
            r'Tarea 1\screenshots\guardar.png')
        time.sleep(1)
        pyautogui.click(*coords_guardar, clicks=1)

context = ssl.create_default_context()


lista_correo = list(DESTINATARIOS.split(','))


archivos = [r'Tarea 1\Noticias salida\economicas.txt',
            r'Tarea 1\Noticias salida\politicas.txt',
            r'Tarea 1\Noticias salida\principales.txt']


destinatarios = ",".join(lista_correo)


for archivo in archivos:

    newMessage = EmailMessage()
    newMessage['From'] = MAIL
    newMessage['To'] = destinatarios
    newMessage['Subject'] = f"Lista de noticias {splitter(archivo)}  del dia de hoy"

    try:
        with open(archivo, 'r') as file:
            file_data = file.read()
            logger_debug.debug(f"Archivo {archivo} leido con exito")
    except Exception as e:
        logger_error.error(e)

    newMessage.set_content(file_data)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        try:
            server.login(MAIL, PASSWORD)
            print(
                f"se ha enviado con exito el mail con las noticias {splitter(archivo)}")
            server.send_message(newMessage)
            logger_debug.debug(
                f"se ha enviado correctamente el correo a {destinatarios}")
        except Exception as e:
            logger_error.error(e)


# BORRAR ARCHIVOS

ruta = r'Tarea 1\Noticias salida\*.txt'
lista_txt = glob.glob(ruta)


for txt in lista_txt:
    if txt.endswith('.txt'):
        try:
            os.remove(txt)
            logger_debug.debug(f"El archivo {txt} ha sido eliminado")

        except Exception as e:
            logger_debug.error(e)
