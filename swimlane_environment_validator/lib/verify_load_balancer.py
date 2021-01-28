#!/usr/bin/env python3
import swimlane_environment_validator.lib.config as config
import swimlane_environment_validator.lib.log_handler as log_handler
import json
import requests
import socket

logger = log_handler.setup_logger()

def verify_dns_resolution(lb_fqdn):
    try:
        logger.debug("Load Balancer FQDN resolved to: {}".format(socket.gethostbyname(lb_fqdn)))
        return True
    except:
        logger.info("Unable to resolve {}".format(lb_fqdn))
        return False

def verify_port_connectivity(port, lb_fqdn):
    logger.info('Checking connectivity for {}:{}'.format(lb_fqdn, port))

    result_name = "{}:{}".format(lb_fqdn, port)
    result = {
        result_name: {}
    }
    
    try:
        r = requests.get('http://{}:{}/health'.format(lb_fqdn, port), timeout=10)
    except:
        logger.error("{}:{} refused the connection..".format(lb_fqdn, port))
        result[result_name]['result'] = "{}Failed{}".format(config.FAIL, config.ENDC)
        return result

    if r.status_code == 200:
        logger.info("{}:{} responded!".format(lb_fqdn, port))
        if json.dumps(r.json()) == '{"status": "ok"}':
            result[result_name]['result'] = "{}Passed{}".format(config.OK, config.ENDC)
        else:
            result[result_name]['result'] = "{}Warning{}".format(config.WARNING, config.ENDC)
            logger.error("{}:{} responded but it didnt match the expected output. Did something else respond to it?".format(lb_fqdn, port))
            logger.error(r.content)

    else:
        logger.error("{}:{} didn't respond with code 200..".format(lb_fqdn, port))
        result[result_name]['result'] = "{}Failed{}".format(config.FAIL, config.ENDC)

    return result