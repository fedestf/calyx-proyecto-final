import smtplib
import ssl
from settings import PASSWORD, MAIL
from loggers import logger_debug, logger_error

context = ssl.create_default_context()


lista_correo = ['makeyourlife@hotmail.com',
                'fede520@live.com']

with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:

    server.login(MAIL, PASSWORD)
    print("se ha logueado con exito")

    for correo in lista_correo:
        try:
            destinatario = correo
            mensaje = ("Hola hijo de puta esto es un mail automatico")
            server.sendmail(MAIL, destinatario, mensaje)
            print(f"Mensaje enviado con exito a {destinatario}")
            logger_debug.debug(f"Mensaje enviado con exito a {destinatario}")
        except Exception as e:
            logger_error.error(e)
