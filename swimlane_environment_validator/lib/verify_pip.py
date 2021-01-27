#!/usr/bin/env python3
import subprocess
import sys
import shutil

import swimlane_environment_validator.lib.config as config
import swimlane_environment_validator.lib.log_handler as log_handler

logger = log_handler.setup_logger()

def create_virtual_env():
    sp = subprocess.check_call(
                                [
                                    "python3",
                                    "-m",
                                    "venv",
                                    "pip-install-test-venv"
                                ],
                                stdout=subprocess.DEVNULL, 
                                stderr=subprocess.STDOUT
                              )

    if config.arguments.pip_config:
        shutil.copyfile(config.arguments.pip_config, 'pip-install-test-venv/pip.conf')

    if sp != 0:
        logger.error("Something went wrong with trying to create a virtualenv. Is virtualenv installed?")
        return False
    else:
        logger.debug("Virtualenv created to test pip with config file")
        return True

def attempt_pip_install():
    result = {}

    if not create_virtual_env():
        result['results'] = "Failed"
        result['message'] = "Failed to configure the venv to test pip with.."
        return result

    sp = subprocess.check_call(
                                [
                                    "pip-install-test-venv/bin/python",
                                    "-m",
                                    "pip",
                                    "download",
                                    "example-package"
                                ],
                                stdout=subprocess.DEVNULL, 
                                stderr=subprocess.STDOUT
                              )

    if sp != 0:
        logger.error("Something went wrong with the pip download command..")
        result['results'] = "Failed"
        result['message'] = "Something went wrong with the pip download command."
    else:
        logger.info("Was able to download example-package from the configured pip repository!")
        result['results'] = "Passed"
        result['message'] = "example-package was able to be downloaded from the configured PyPi server."
    
    return result