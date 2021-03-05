#!/usr/bin/env python3
import tempfile
import os
import shutil
import time
import sys
import json

import swimlane_environment_validator.lib.config as config
import swimlane_environment_validator.lib.log_handler as log_handler

import swimlane_environment_validator.lib.verify_disk_space as verify_disk_space
import swimlane_environment_validator.lib.verify_load_balancer as verify_load_balancer
import swimlane_environment_validator.lib.verify_pip as verify_pip
import swimlane_environment_validator.lib.verify_ntp as verify_ntp
import swimlane_environment_validator.lib.verify_public_endpoints as verify_public_endpoints
import swimlane_environment_validator.lib.parse_installer_yaml as parse_installer_yaml
import swimlane_environment_validator.lib.verify_executables as verify_executables
import swimlane_environment_validator.lib.verify_cluster_ports as verify_cluster_ports
import swimlane_environment_validator.lib.verify_tls as verify_tls

import swimlane_environment_validator.lib.http_listener as http_listener

import swimlane_environment_validator.lib.table as table

logger = log_handler.setup_logger()

check_results = {
    "checks": {
        "directory_size_checks": {},
        "is_own_partition_checks": {},
        "load_balancer_port_checks": {},
        "pip_checks": {},
        "swimlane_certificate_checks": {},
        "kots_certificate_checks": {},
        "additional_certificate_checks": {},
        "public_endpoint_checks": {},
        "ntp_checks": {},
        "hostnamectl_checks": {},
        "disallowed_executables": {},
        "intra_port_connectivity": {},
        "http_proxy_config":{}
    }
}

def main():
    logger.info('Starting Swimlane SPI environment verification...')

    if config.arguments.command == 'verify':

        logger.debug('Installer patch yaml: {}'.format(config.installer_yaml))

        check_results['checks']['http_proxy_config'].update(parse_installer_yaml.verify_installer_yaml_proxies())

        logger.debug('Creating temporary directory')
        tmp_path = tempfile.mkdtemp()
        logger.debug('Temp dir: {}'.format(tmp_path))
        if config.arguments.pip_config:
            try:
                shutil.copyfile(config.arguments.pip_config, '{}/pip.conf'.format(tmp_path))
            except FileNotFoundError:
                logger.warning("Couldn't find file {} for pip config, continuing without it...".format(config.arguments.pip_config))
        os.chdir(tmp_path)

        if config.arguments.verify_public_endpoints and not config.arguments.offline:
            check_results['checks']['public_endpoint_checks'].update(verify_public_endpoints.check_endpoints(config.PUBLIC_ENDPOINTS))

        if config.arguments.verify_disk_space:
            check_results['checks']['directory_size_checks'].update(verify_disk_space.check_directory_size())

        if config.arguments.verify_disk_space:
            check_results['checks']['is_own_partition_checks'].update(verify_disk_space.check_if_mount())

        if config.arguments.verify_pip:
            check_results['checks']['pip_checks'].update(verify_pip.attempt_pip_install())

        if config.arguments.verify_ntp:
            check_results['checks']['ntp_checks'].update(verify_ntp.get_service_status())

        if config.arguments.verify_lb:
            if config.arguments.enable_listeners:
                http_listener.start_lb_listener_threads()
                logger.info('Sleeping for {} seconds to allow LB to see that we are live'.format(config.arguments.lb_delay_period))
                time.sleep(config.arguments.lb_delay_period)
            check_results['checks']['load_balancer_port_checks'].update(verify_load_balancer.verify_port_connectivity())

        if config.arguments.verify_executables:
            check_results['checks']['disallowed_executables'].update(verify_executables.check_installed_executables(config.UNALLOWED_EXECUTABLES))

        if config.arguments.verify_intra_cluster_ports and config.arguments.additional_node_fqdn:
            check_results['checks']['intra_port_connectivity'].update(verify_cluster_ports.verify_port_connectivity())

        if config.arguments.verify_swimlane_tls_certificate:
            check_results['checks']['swimlane_certificate_checks'].update(verify_tls.get_certificate_info())

        logger.debug('Cleaning up temporary directory')
        shutil.rmtree(tmp_path)
        logger.debug(json.dumps(check_results, sort_keys=True, indent=4))

        table.print_table(check_results['checks'])

    if config.arguments.command == 'listener':
        http_listener.start_lb_listener_threads()
        http_listener.start_intra_cluster_listener_threads()
        input("Web and Intra-Cluster Listeners are running, press enter to exit.")

if __name__ == "__main__":
    main()
