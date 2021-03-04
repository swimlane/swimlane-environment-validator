import requests

import swimlane_environment_validator.lib.config as config
import swimlane_environment_validator.lib.log_handler as log_handler

import swimlane_environment_validator.lib.parse_installer_yaml as parse_installer_yaml

logger = log_handler.setup_logger()

def get_endpoint(endpoint_url, acceptable_status_code):
    logger.info('Checking connectivity to {}'.format(endpoint_url))

    endpoint_result = {
        "result" : "Skipped"
    }

    try:
        r = requests.get(endpoint_url, timeout=10, allow_redirects=False, proxies=parse_installer_yaml.get_proxies())
    except:
        logger.error('Response from {} timed out or failed after 10s.'.format(endpoint_url))
        logger.debug("Caught exception during endpoint check", exc_info=True)
        endpoint_result['status_code'] = "-"
        endpoint_result['result'] = "{}Failed{}".format(config.FAIL, config.ENDC)
        return endpoint_result

    logger.debug(r.status_code)

    endpoint_result['status_code'] = r.status_code

    if r.status_code == acceptable_status_code:
        logger.info('Response from {} is ok'.format(endpoint_url))
        endpoint_result['result'] = "{}Passed{}".format(config.OK, config.ENDC)
    else:
        logger.error('Response from {} is not ok'.format(endpoint_url))
        endpoint_result['result'] = "{}Failed{}".format(config.FAIL, config.ENDC)

    return endpoint_result


def check_endpoints(PUBLIC_ENDPOINTS):
    results = {}

    for endpoint in PUBLIC_ENDPOINTS:
        r = get_endpoint(endpoint['endpoint'], endpoint['status_code'])
        results[endpoint['endpoint']] = r

    return results