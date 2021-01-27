#!/usr/bin/env python3
import swimlane_environment_validator.lib.config as config
import swimlane_environment_validator.lib.log_handler as log_handler
import subprocess
from shutil import which

logger = log_handler.setup_logger()

def check_service_running(service):
    p =  subprocess.Popen(["systemctl", "is-active",  service], stdout=subprocess.PIPE)
    (output, err) = p.communicate()
    output = output.decode('utf-8')

    if output == "active":
        logger.debug('{} is active'.format(service))
        return True
    else:
        logger.debug('{} is inactive'.format(service))
        return False

def check_service_enabled(service):
    p =  subprocess.Popen(["systemctl", "is-enabled",  service], stdout=subprocess.PIPE)
    (output, err) = p.communicate()
    output = output.decode('utf-8')

    if output == "enabled":
        logger.debug('{} is enabled'.format(service))
        return True
    else:
        logger.debug('{} is disabled'.format(service))
        return False

def check_service_binary(service):
    return which(service) is not None

def get_service_status():
    results = {}
    for ntp_executable in config.NTP_EXECUTABLES:
        results[ntp_executable] = {}
        results[ntp_executable]['running'] = "{}False{}".format(config.FAIL, config.ENDC)
        results[ntp_executable]['enabled'] = "{}False{}".format(config.FAIL, config.ENDC)

        if check_service_binary(ntp_executable):
            results[ntp_executable]['installed'] = "{}True{}".format(config.OK, config.ENDC)
            if check_service_running(ntp_executable):
                results[ntp_executable]['running'] = "{}True{}".format(config.OK, config.ENDC)
            else:
                results[ntp_executable]['running'] = "{}False{}".format(config.FAIL, config.ENDC)

            if check_service_running(ntp_executable):
                results[ntp_executable]['enabled'] = "{}True{}".format(config.OK, config.ENDC)
            else:
                results[ntp_executable]['enabled'] = "{}False{}".format(config.FAIL, config.ENDC)

        else:
            results[ntp_executable]['installed'] = "{}False{}".format(config.FAIL, config.ENDC)

    return results