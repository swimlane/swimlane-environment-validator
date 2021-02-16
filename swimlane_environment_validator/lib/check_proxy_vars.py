import swimlane_environment_validator.lib.config as config
import swimlane_environment_validator.lib.log_handler as log_handler
from os import environ

logger = log_handler.setup_logger()

def check_var(var):
    if environ.get(var) is None:
        logger.debug('Environment variable, will not use this proxy.')
        return "-"
    else:
        logger.info('Environment variable found, if will use this proxy')
        return "{}".format(environ.get(var))

def check_proxy_vars():

    results = {
        "HTTP_PROXY": {
            "message": check_var('HTTP_PROXY')
        },
        "HTTPS_PROXY": {
            "message": check_var('HTTPS_PROXY')
        },
        "http_proxy": {
            "message": check_var('http_proxy')
        },
        "https_proxy": {
            "message": check_var('https_proxy')
        }
    }

    return results
