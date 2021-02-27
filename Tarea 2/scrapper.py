from bs4 import BeautifulSoup
import requests
from loggers import logger_debug, logger_error

# SCRAPPING PRINCIPAL
url_principal = 'https://www.infobae.com/'
page = requests.get(url_principal)
soup = BeautifulSoup(page.content, 'html.parser')

titular = soup.find_all('h2', class_="headline-title")


for elem in titular:

    sub = elem.find_all('a')

    with open(r'Tarea 2\Noticias salida\principal.txt', "a") as file:

        try:

            file.write("\n"+sub[0].getText())  # textos de la etiqueta a
            # concateno el link de la pagina al href
            file.write("\n"+"https://www.infobae.com" +
                       sub[0].get('href')+"\n")
            logger_debug.debug(
                f"Se añadio correctamente la noticia {sub[0].getText()}")

        except Exception as e:
            logger_error.error(e)

# SCRAPPING POLITICA

url_politica = 'https://www.infobae.com/politica/'
page = requests.get(url_politica)
soup = BeautifulSoup(page.content, 'html.parser')

titular = soup.find_all('h2', class_="headline-title")


for elem in titular:

    sub = elem.find_all('a')

    if sub[0].get('href').startswith('/politica'):  # SI HREF EMPIEZA CON /economia

        with open(r'Tarea 2\Noticias salida\politica.txt', "a") as file:

            try:

                file.write("\n"+sub[0].getText())  # textos de la etiqueta a
                # concateno el link de la pagina al href
                file.write("\n"+"https://www.infobae.com" +
                           sub[0].get('href')+"\n")
                logger_debug.debug(
                    f"Se añadio correctamente la noticia {sub[0].getText()}")

            except Exception as e:
                logger_error.error(e)

# SCRAPPING ECONOMIA

url_economia = 'https://www.infobae.com/economia/'
page = requests.get(url_economia)
soup = BeautifulSoup(page.content, 'html.parser')

titular = soup.find_all('h2', class_="headline-title")


for elem in titular:

    sub = elem.find_all('a')

    if sub[0].get('href').startswith('/economia'):  # SI HREF EMPIEZA CON /economia

        with open(r'Tarea 2\Noticias salida\economia.txt', "a") as file:

            try:

                file.write("\n"+sub[0].getText())  # textos de la etiqueta a
                # concateno el link de la pagina al href
                file.write("\n"+"https://www.infobae.com" +
                           sub[0].get('href')+"\n")
                logger_debug.debug(
                    f"Se añadio correctamente la noticia {sub[0].getText()}")

            except Exception as e:
                logger_error.error(e)
