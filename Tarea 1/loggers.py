import logging
from settings import RUTA
import os
from datetime import date

# logging.basicConfig(filename=r"C:\Users\fedestf\Documents\GitHub\python-rpa-calyx\Clase 6\logs.txt",
#                     format="'%(levelname)s : %(asctime)s - %(message)s'")


# Custom logger

# Creo subdirectorio (en caso de que no exista) a partir de la ruta de logs definida en settings
# carpeta_error = os.path.join(RUTA, "Nombre carpeta")

# # Declaro la ruta  y el nombre del archivo para pasarlo al file handler
# # Ahora mi ruta es la carpeta creada antes

# ruta = os.path.join(carpeta, date.today().strftime("%d-%m-%Y")+".txt")

# logger_debug.info("INFO")
# logger_debug.debug("DEBUG")
# logger_debug.critical("CRITICAL")
# logger_debug.error("ERROR")
# logger_debug.warning("WARNING")

# ----------------------TEST ERROR-------------------------

carpeta_error = os.path.join(RUTA, "Error")

if not os.path.exists(carpeta_error):
    os.makedirs(carpeta_error)

ruta = os.path.join(carpeta_error,
                    date.today().strftime("%d-%m-%Y") + ".txt")

logger_error = logging.getLogger("test_error")
file_hand = logging.FileHandler(ruta)

format_hand = logging.Formatter(
    '%(levelname)s : %(asctime)s.%(msecs)03d -  [%(funcName)s]- %(message)s', "%d-%m-%Y %H:%M:%S")

file_hand.setFormatter(format_hand)
logger_error.addHandler(file_hand)


# ---------------------TEST DEBUG--------------------------------------


carpeta_debug = os.path.join(RUTA, "Debug")

if not os.path.exists(carpeta_debug):
    os.makedirs(carpeta_debug)

ruta = os.path.join(carpeta_debug,
                    date.today().strftime("%d-%m-%Y") + ".txt")

logger_debug = logging.getLogger("test_debug")
file_hand = logging.FileHandler(ruta)

file_hand.setFormatter(format_hand)  # Reutilizo el formatter
logger_debug.addHandler(file_hand)
logger_debug.setLevel(logging.DEBUG)
