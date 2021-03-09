from loggers import logger_debug, logger_error
import smtplib
import ssl
from email.message import EmailMessage
import glob
from funciones import splitter
import os


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
