#!/usr/bin/env python3
import swimlane_environment_validator.lib.config as config
import swimlane_environment_validator.lib.log_handler as log_handler
import os

logger = log_handler.setup_logger()

def check_directory_size():
    results = {}
    for directory,minimum_size in config.DIRECTORY_SIZES_CHECK.items():
        logger.debug('Checking size of {}'.format(directory))

        result = {}

        try:
            df_output_lines = [s.split() for s in os.popen("df -BG {}".format(directory)).read().splitlines()]
            total = df_output_lines[1][1]
            used = df_output_lines[1][2]
            free = df_output_lines[1][3]
            percentage = df_output_lines[1][4]
        except:
            logger.error('{} cannot be found.'.format(directory))
            result['Total Space Size'] = "-"
            result['Percentage Used'] = "-"
            result['message'] = "{} could not be found".format(directory)
            result['minimum'] = minimum_size
            result['result'] = "{}Failed{}".format(config.FAIL, config.ENDC)
            results[directory] = result
            continue

        logger.debug('Partition size \nTotal: {total}\nUsed: {used}\nFree: {free}, Percentage Used: {percentage}'.format(
            total=total,
            used=used,
            free=free,
            percentage=percentage
            )
        )

        result['Total Space Size'] = total
        result['Percentage Used'] = percentage

        if int(total.replace('G','')) >= int(minimum_size.replace('G','')):
            logger.info('{} has at least {} worth of space.'.format(directory, minimum_size))
            result['message'] = "-"
            result['minimum'] = minimum_size
            result['result'] = "{}Passed{}".format(config.OK, config.ENDC)
        else:
            logger.error('{} is less than {} worth of space'.format(directory, minimum_size))
            result['message'] = "{} is not large enough to meet minimum requirements.".format(directory)
            result['minimum'] = minimum_size
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