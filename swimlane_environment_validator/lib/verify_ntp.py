#!/usr/bin/env python3
import swimlane_environment_validator.lib.config as config
import swimlane_environment_validator.lib.log_handler as log_handler
import subprocess
from shutil import which

logger = log_handler.setup_logger()

def check_service_running(service):

    sp = subprocess.Popen(
                                [
                                    "systemctl",
                                    "is-active",
                                    service
                                ],
                                stdout=subprocess.DEVNULL, 
                                stderr=subprocess.STDOUT
                              )

    streamdata = sp.communicate()[0]
    logger.debug('{} enabled return code: {}'.format(service, sp.returncode))
    if sp.returncode == 0:
        logger.debug('{} is active'.format(service))
        return True
    else:
        logger.debug('{} is inactive'.format(service))
        return False

def check_service_enabled(service):

    sp = subprocess.Popen(
                                [
                                    "systemctl",
                                    "is-enabled",
                                    service
                                ],
                                stdout=subprocess.DEVNULL, 
                                stderr=subprocess.STDOUT
                              )

    streamdata = sp.communicate()[0]
    logger.debug('{} enabled return code: {}'.format(service, sp.returncode))
    if sp.returncode == 0:
        logger.debug('{} is enabled'.format(service))
        return True
    else:
        logger.debug('{} is disabled'.format(service))
        return False

def get_service_status():
    results = {}
    for ntp_executable in config.NTP_EXECUTABLES:
        results[ntp_executable] = {}
        results[ntp_executable]['running'] = "{}False{}".format(config.FAIL, config.ENDC)
        results[ntp_executable]['enabled'] = "{}False{}".format(config.FAIL, config.ENDC)

        if check_service_running(ntp_executable):
            results[ntp_executable]['running'] = "{}True{}".format(config.OK, config.ENDC)
        else:
            results[ntp_executable]['running'] = "{}False{}".format(config.FAIL, config.ENDC)

        if check_service_enabled(ntp_executable):
            results[ntp_executable]['enabled'] = "{}True{}".format(config.OK, config.ENDC)
        else:
            results[ntp_executable]['enabled'] = "{}False{}".format(config.FAIL, config.ENDC)

    return results