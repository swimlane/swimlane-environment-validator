#!/usr/bin/env python3
import swimlane_environment_validator.lib.config as config
import swimlane_environment_validator.lib.log_handler as log_handler
import shutil
import os

logger = log_handler.setup_logger()

def check_directory_size(directory, minimum_bytes):
    logger.debug('Checking size of {}'.format(directory))

    results = {
        directory: {}
    }

    try:
        total, used, free = shutil.disk_usage(directory)
    except FileNotFoundError:
        logger.error('{} cannot be found.'.format(directory))
        results[directory]['Total Space Size'] = "-"
        results[directory]['Percentage Used'] = "-"
        results[directory]['message'] = "{} could not be found".format(directory)
        results[directory]['result'] = "{}Failed{}".format(config.FAIL, config.ENDC)
        return results

    logger.debug('Partition size \nTotal: {total}\nUsed: {used}\nFree: {free}, Percentage Used: {percentage}'.format(
        total=( total / 1024 / 1024 / 1024 ),
        used=( used / 1024 / 1024 / 1024 ),
        free=( free / 1024 / 1024 / 1024 ),
        percentage=( ( used / total ) * 100 )
        )
    )

    results[directory]['Total Space Size'] = ( total / 1024 / 1024 / 1024 )
    results[directory]['Percentage Used'] = ( ( used / total ) * 100 )

    if total >= minimum_bytes:
        logger.info('{} has at least {} bytes available.'.format(directory, minimum_bytes))
        results[directory]['message'] = "-"
        results[directory]['result'] = "{}Passed{}".format(config.OK, config.ENDC)
    else:
        logger.error('{} has less {} bytes available.'.format(directory, minimum_bytes))
        results[directory]['message'] = "{} is not large enough to meet minimum requirements.".format(directory)
        results[directory]['result'] = "{}Failed{}".format(config.FAIL, config.ENDC)

    return results

def check_if_mount(directory):
    results = {
        directory: {}
    }

    is_mount = os.path.ismount(directory)

    if is_mount:
        results[directory]['message'] = "{} is a mount.".format(directory)
        results[directory]['result'] = "{}Passed{}".format(config.OK, config.ENDC)
    else:
        results[directory]['message'] = "{} is not a mounted directory.".format(directory)
        results[directory]['result'] = "{}Failed{}".format(config.FAIL, config.ENDC)

    return results