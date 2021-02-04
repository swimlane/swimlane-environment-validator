#!/usr/bin/env python3
import subprocess
import sys
import shutil
import os

import swimlane_environment_validator.lib.config as config
import swimlane_environment_validator.lib.log_handler as log_handler

logger = log_handler.setup_logger()

def create_virtual_env():

    try:
        sp = subprocess.Popen(
                                    [
                                        "python3",
                                        "-m",
                                        "virtualenv",
                                        "pip-install-test-venv"
                                    ],
                                    stdout=subprocess.DEVNULL, 
                                    stderr=subprocess.STDOUT
                                  )

        streamdata = sp.communicate()[0]
    except FileNotFoundError:
        logger.error("Something went wrong with trying to create a virtualenv. Is python3 and python3-virtualenv installed?")
        return False

    if config.arguments.verify_pip:
        try:
            shutil.copyfile(config.arguments.pip_config, 'pip-install-test-venv/pip.conf')
        except FileNotFoundError:
            logger.warning("Couldn't find file {} for pip config, continuing without it...".format(config.arguments.pip_config))

    if sp.returncode != 0:
        logger.error("Something went wrong with trying to create a virtualenv. Is virtualenv installed?")
        return False
    else:
        logger.debug("Virtualenv created to test pip with config file")
        return True

def attempt_pip_install():
    result = {
        "pip" : {}
    }

    if not create_virtual_env():
        result['pip']['message'] = "Failed to configure the venv to test pip with, is python3-virtualenv installed?"
        result['pip']['results'] = "{}Failed{}".format(config.FAIL, config.ENDC)
        return result

    sp = subprocess.Popen(
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

    streamdata = sp.communicate()[0]
    if sp.returncode != 0:
        logger.error("Something went wrong with the pip download command..")
        result['pip']['message'] = "Something went wrong with the pip download command."
        result['pip']['results'] = "{}Failed{}".format(config.FAIL, config.ENDC)
    else:
        logger.info("Was able to download example-package from the configured pip repository!")
        result['pip']['message'] = "example-package was able to be downloaded from the configured PyPi server."
        result['pip']['results'] = "{}Passed{}".format(config.OK, config.ENDC)
    
    return result
