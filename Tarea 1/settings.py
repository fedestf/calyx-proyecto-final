from decouple import config

RUTA = config('LOG_PATH')
MAIL = config('USER_MAIL')
PASSWORD = config('PASS_MAIL')
DESTINATARIOS = config('DESTINATARIOS')
CALYX_INVOICES_PATH = config('CALYX_INVOICES_PATH')
