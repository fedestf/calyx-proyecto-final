from loggers import logger_debug, logger_error
# agrego un valor a la lista para poder borrarlo y que tome el primer nombre como posicion 0
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
