import swimlane_environment_validator.lib.config as config
import swimlane_environment_validator.lib.log_handler as log_handler
from os import environ

logger = log_handler.setup_logger()

def get_proxies():
    proxies = {
        'http': None,
        'https': None,
        'ftp': None
    }

    if config.arguments.proxy_override:
        logger.debug('--proxy-override was defined, setting proxies to {}'.format(config.arguments.proxy_override))
        proxies['http'] = config.arguments.proxy_override
        proxies['https'] = config.arguments.proxy_override

    else:
        if config.installer_yaml:
            try:
                proxies['http'] = config.installer_yaml['spec']['kurl']['proxyAddress']
                proxies['https'] = config.installer_yaml['spec']['kurl']['proxyAddress']
            except:
                logger.debug('Caught exception when checking for proxy in installer yaml', exc_info=True)
                logger.info('Installer patch found, but no proxy addresses listed, not using a proxy.')
                logger.info('If this is unexpected, check that your patch yaml file is correctly formatted.')
    
    return proxies

def verify_installer_yaml_proxies():
    results = {}
    proxies = get_proxies()

    results['http'] = str(proxies['http'])
    results['https'] = str(proxies['https'])

    return results