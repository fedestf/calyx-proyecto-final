import smtplib
import ssl
from settings import PASSWORD, MAIL
from loggers import logger_debug, logger_error
from email.message import EmailMessage
import os
import glob
import scrapper
from funciones import splitter
from datetime import date


context = ssl.create_default_context()


lista_correo = ['fede520@live.com',
                # 'moreyrajuanse@gmail.com',
                # 'soria.lucas.e@gmail.com',
                # 'moreyrajuanse@gmail.com',
                # 'mariano.river@live.com.ar'
                ]

archivos = [r'Tarea 2\Noticias salida\economicas.txt',
            r'Tarea 2\Noticias salida\politicas.txt',
            r'Tarea 2\Noticias salida\principales.txt']


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

ruta = r'Tarea 2\Noticias salida\*.txt'
lista_txt = glob.glob(ruta)


for txt in lista_txt:
    if txt.endswith('.txt'):
        try:
            os.remove(txt)
            logger_debug.debug(f"El archivo {txt} ha sido eliminado")

        except Exception as e:
            logger_debug.error(e)
