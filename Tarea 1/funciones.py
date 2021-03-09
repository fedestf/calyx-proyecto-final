import tabula
import pandas as pd
import xml.etree.ElementTree as ET
import glob
import json
import pyautogui
from datetime import date
import time
from loggers import logger_debug, logger_error
import smtplib
import ssl
from email.message import EmailMessage
import os
from settings import CALYX_INVOICES_PATH

# agrego un valor a la lista en la funcion splitter
# para poder borrarlo y que tome el primer nombre como posicion 0
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

    try:
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

        logger_debug.debug("Funcion ejecutada correctamente")

        return lista_precios

    except Exception as e:
        logger_error.error(e)


def carga_id_y_fecha(id_factura, dia, mes, año):
    try:
        time.sleep(3)
        pyautogui.hotkey('win', 'd')
        time.sleep(2)
        pyautogui.hotkey('win', 'r')
        time.sleep(2)
        pyautogui.write(CALYX_INVOICES_PATH, interval=0.50)
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(3)
        coords_id_factura = pyautogui.locateCenterOnScreen(
            r'Tarea 1\screenshots\id_factura.png')

        pyautogui.click(*coords_id_factura, clicks=1)
        time.sleep(1)
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
                r'Tarea 1\screenshots\agregar_item.png')
            pyautogui.click(*coords_agregar_item, clicks=1)

            coords_0_fondo_azul = pyautogui.locateCenterOnScreen(
                r'Tarea 1\screenshots\0_fondo_azul.png')
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
                r'Tarea 1\screenshots\agregar_item.png')
            pyautogui.click(*coords_agregar_item, clicks=1)

            coords_0_fondo_azul = pyautogui.locateCenterOnScreen(
                r'Tarea 1\screenshots\0_fondo_azul.png')
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
                r'Tarea 1\screenshots\agregar_item.png')
            pyautogui.click(*coords_agregar_item, clicks=1)

            coords_0_fondo_azul = pyautogui.locateCenterOnScreen(
                r'Tarea 1\screenshots\0_fondo_azul.png')
            time.sleep(2)
            pyautogui.click(*coords_0_fondo_azul, clicks=1)
            time.sleep(2)

        logger_debug.debug("Funcion ejecutada correctamente")

    except Exception as e:
        logger_error.error(e)


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

        logger_debug.debug("Carga de producto correcta")

    except Exception as e:
        logger_error.error(e)


def correo_facturas(facturas_correctas, destinatarios, usuario, password):

    try:
        context = ssl.create_default_context()
        lista_correo = list(destinatarios.split(','))
        destinatario = ",".join(lista_correo)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:

            newMessage = EmailMessage()
            newMessage['From'] = usuario
            newMessage['To'] = destinatario
            newMessage['Subject'] = "Facturas cargadas correctamente"

            try:
                server.login(usuario, password)
                mensaje = str(facturas_correctas).replace(
                    "[", "").replace("]", "").replace("'", "")
                newMessage.set_content(mensaje)
                server.send_message(newMessage)

                logger_debug.debug(
                    f"Mensaje enviado con exito a {destinatario}")
            except Exception as e:
                logger_error.error(e)

        logger_debug.debug("ejecutado correctamente")

    except Exception as e:
        logger_error.error(e)


def mail_noticias(archivos, destinatarios, usuario, password):
    try:
        context = ssl.create_default_context()
        lista_correo = list(destinatarios.split(','))
        destinatarios = ",".join(lista_correo)

        for archivo in archivos:

            newMessage = EmailMessage()
            newMessage['From'] = usuario
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
                    server.login(usuario, password)
                    print(
                        f"se ha enviado con exito el mail con las noticias {splitter(archivo)}")
                    server.send_message(newMessage)
                    logger_debug.debug(
                        f"se ha enviado correctamente el correo a {destinatarios}")
                except Exception as e:
                    logger_error.error(e)

        logger_debug.debug("Noticias enviadas correctamente")

        ruta = r'Tarea 1\Noticias salida\*.txt'
        lista_txt = glob.glob(ruta)

        for txt in lista_txt:
            if txt.endswith('.txt'):
                try:
                    os.remove(txt)
                    logger_debug.debug(f"El archivo {txt} ha sido eliminado")

                except Exception as e:
                    logger_debug.error(e)
    except Exception as e:
        logger_error.error(e)
