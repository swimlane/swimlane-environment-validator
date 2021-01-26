import lib.config as config
import lib.log_handler as log_handler
from os import environ

logger = log_handler.setup_logger()

def check_var(var):
    if environ.get(var) is None:
        logger.debug('Env Var {} not found, will not use this proxy.'.format(var))
        return "{} is not set.".format(var)
    else:
        logger.info('Env Var {} found, if will use this proxy'.format(var))
        return "{} is set to {}.".format(var, environ.get(var))

def check_proxy_vars():

    results = {
        "HTTP_PROXY": {
            "result": "-",
            "message": check_var('HTTP_PROXY')
        },
        "HTTPS_PROXY": {
            "result": "-",
            "message": check_var('HTTPS_PROXY')
        },
        "http_proxy": {
            "result": "-",
            "message": check_var('http_proxy')
        },
        "https_proxy": {
            "result": "-",
            "message": check_var('https_proxy')
        }
    }

    return results