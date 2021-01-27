#!/usr/bin/env python3
import os
import swimlane_environment_validator.lib.config as config
import swimlane_environment_validator.lib.log_handler as log_handler
from shutil import which
logger = log_handler.setup_logger()

def get_executable(name):
    """Check whether `name` is on PATH and marked as executable."""

    return which(name)

def check_installed_executables(executables):
    logger.debug('Checking for executables {}'.format(config.UNALLOWED_EXECUTABLES))
    results = {}

    for exe in executables:
        result = {
            'path': '-',
            'message': '-'
        }

        r = get_executable(exe)
        
        if r is not None:
            logger.debug('{} is installed but is not allowed'.format(r))
            result['result'] = "{}Failed{}".format(config.FAIL, config.ENDC)
            result['message'] = "{} is not allowed to be pre-installed".format(exe)
            result['path'] = r
        else:
            logger.debug('{} is not installed.'.format(exe))
            result['result'] = "{}Passed{}".format(config.OK, config.ENDC)
        
        results[exe] = result

    return results