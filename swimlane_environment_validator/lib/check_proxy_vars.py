import swimlane_environment_validator.lib.config as config
import swimlane_environment_validator.lib.log_handler as log_handler
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
            "message": check_var('HTTP_PROXY'),
            "result": "-",
        },
        "HTTPS_PROXY": {
            "message": check_var('HTTPS_PROXY'),
            "result": "-",
        },
        "http_proxy": {
            "message": check_var('http_proxy'),
            "result": "-",
        },
        "https_proxy": {
            "message": check_var('https_proxy'),
            "result": "-",
        }
    }

    return results