import smtplib
import ssl
from settings import PASSWORD, MAIL
from loggers import logger_debug, logger_error
from email.message import EmailMessage

context = ssl.create_default_context()


lista_correo = ['fede520@live.com',
                'moreyrajuanse@gmail.com',
                'soria.lucas.e@gmail.com',
                'moreyrajuanse@gmail.com',
                'mariano.river@live.com.ar'
                ]

destinatarios = ",".join(lista_correo)

newMessage = EmailMessage()
newMessage['Subject'] = "Lista de noticias de economia de la fecha"
newMessage['From'] = MAIL
newMessage['To'] = destinatarios

with open(r'Tarea 2\Noticias salida\economia.txt', 'r') as file:
    file_data = file.read()
    # file_name = "economia.pdf"

newMessage.set_content(file_data)

# newMessage.add_attachment(
#     file_data, maintype='application', subtype='octet-stream', filename=file_name)

with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    try:
        server.login(MAIL, PASSWORD)
        print("se ha logueado con exito")
        server.login(MAIL, PASSWORD)
        server.send_message(newMessage)
        logger_debug.debug(
            f"se ha enviado correctamente el correo a {destinatarios}")
    except Exception as e:
        logger_error.error(e)

    # for correo in lista_correo:
    #     try:

    #         destinatario = correo
    #         mensaje = ("Hola hijo de puta esto es un mail automatico")

    #         server.sendmail(MAIL, destinatario, mensaje)
    #         print(f"Mensaje enviado con exito a {destinatario}")
    #         logger_debug.debug(f"Mensaje enviado con exito a {destinatario}")
    #     except Exception as e:
    #         logger_error.error(e)
