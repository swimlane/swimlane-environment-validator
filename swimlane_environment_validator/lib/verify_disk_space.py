#!/usr/bin/env python3
import swimlane_environment_validator.lib.config as config
import swimlane_environment_validator.lib.log_handler as log_handler
import shutil
import os

logger = log_handler.setup_logger()

def check_directory_size():
    results = {}
    for directory,minimum_bytes in config.DIRECTORY_SIZES_CHECK.items():
        logger.debug('Checking size of {}'.format(directory))

        result = {}

        try:
            total, used, free = shutil.disk_usage(directory)
        except FileNotFoundError:
            logger.error('{} cannot be found.'.format(directory))
            result['Total Space Size'] = "-"
            result['Percentage Used'] = "-"
            result['message'] = "{} could not be found".format(directory)
            result['result'] = "{}Failed{}".format(config.FAIL, config.ENDC)
            results[directory] = result
            continue

        logger.debug('Partition size \nTotal: {total}\nUsed: {used}\nFree: {free}, Percentage Used: {percentage}'.format(
            total=( total / 1024 / 1024 / 1024 ),
            used=( used / 1024 / 1024 / 1024 ),
            free=( free / 1024 / 1024 / 1024 ),
            percentage=( ( used / total ) * 100 )
            )
        )

        result['Total Space Size'] = ( total / 1024 / 1024 / 1024 )
        result['Percentage Used'] = ( ( used / total ) * 100 )

        if total >= minimum_bytes:
            logger.info('{} has at least {} bytes available.'.format(directory, minimum_bytes))
            result['message'] = "-"
            result['result'] = "{}Passed{}".format(config.OK, config.ENDC)
        else:
            logger.error('{} has less {} bytes available.'.format(directory, minimum_bytes))
            result['message'] = "{} is not large enough to meet minimum requirements.".format(directory)
            result['result'] = "{}Failed{}".format(config.FAIL, config.ENDC)
        results[directory] = result
    return results

def check_if_mount():
    results = {}
    for directory in config.DIRECTORY_IS_MOUNT_CHECK:
        result = {}

        is_mount = os.path.ismount(directory)

        if is_mount:
            result['message'] = "{} is a mount.".format(directory)
            result['result'] = "{}Passed{}".format(config.OK, config.ENDC)
        else:
            result['message'] = "{} is not a mounted directory.".format(directory)
            result['result'] = "{}Failed{}".format(config.FAIL, config.ENDC)
        results[directory] = result

    return results