import logging
from settings import RUTA
import os
from datetime import date

# -----------ERROR--------------

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


# -----------DEBUG--------------


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
