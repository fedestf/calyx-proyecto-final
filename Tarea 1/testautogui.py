import json
import pyautogui
import time
from datetime import date


# reemplazar los print por instrucciones al robot


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
