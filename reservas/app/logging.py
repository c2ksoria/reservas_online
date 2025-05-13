import logging

# Obtener un logger
logger_info = logging.getLogger(__name__)
logger_error = logging.getLogger('django')

def mostrar(mensaje):
    # Registro de información general
    logger_info.info(mensaje)
    print("prueba...")
    # try:
    #     # Algo que puede lanzar un error
    #     resultado = 10 / 0
    # except Exception as e:
    #     # Registro de errores
    #     logger_error.error('Ocurrió un error: %s', str(e), exc_info=True)
