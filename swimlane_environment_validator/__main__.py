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
import swimlane_environment_validator.lib.verify_tls as verify_tls
import swimlane_environment_validator.lib.verify_pip as verify_pip
import swimlane_environment_validator.lib.verify_ntp as verify_ntp
import swimlane_environment_validator.lib.verify_public_endpoints as verify_public_endpoints
import swimlane_environment_validator.lib.check_proxy_vars as check_proxy_vars

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
        "proxy_env_var_checks": {}
    }
}

def main():
    logger.info('Starting Swimlane SPI environment verification...')

    if config.arguments.command == 'verify':

        check_results['checks']['proxy_env_var_checks'].update(check_proxy_vars.check_proxy_vars())

        logger.debug('Creating temporary directory')
        tmp_path = tempfile.mkdtemp()
        if config.arguments.pip_config:
            shutil.copyfile(config.arguments.pip_config, '{}/pip.conf'.format(tmp_path))
        os.chdir(tmp_path)

        if config.arguments.verify_public_endpoints and not config.arguments.offline:
            check_results['checks']['public_endpoint_checks'].update(verify_public_endpoints.check_endpoints(config.PUBLIC_ENDPOINTS))

        if config.arguments.verify_swimlane_tls_certificate:
            check_results['checks']['swimlane_certificate_checks'].update(
                verify_tls.verify_certificate_key(
                    config.arguments.swimlane_certificate,
                    config.arguments.swimlane_key
                )
            )

        if config.arguments.verify_disk_space:
            check_results['checks']['directory_size_checks'].update(verify_disk_space.check_directory_size('/var/openebs', (300 * 1024 * 1024 * 1024 )))
            check_results['checks']['directory_size_checks'].update(verify_disk_space.check_directory_size('/var/lib/docker', (100 * 1024 * 1024 * 1024 )))
            check_results['checks']['directory_size_checks'].update(verify_disk_space.check_directory_size('/opt', (50 * 1024 * 1024 * 1024 )))
            check_results['checks']['directory_size_checks'].update(verify_disk_space.check_directory_size('/', (50 * 1024 * 1024 * 1024 )))

        if config.arguments.verify_disk_space:
            check_results['checks']['is_own_partition_checks'].update(verify_disk_space.check_if_mount('/var/openebs'))
            check_results['checks']['is_own_partition_checks'].update(verify_disk_space.check_if_mount('/var/lib/docker'))
            check_results['checks']['is_own_partition_checks'].update(verify_disk_space.check_if_mount('/opt'))

        if config.arguments.verify_pip:
            check_results['checks']['pip_checks'].update(verify_pip.attempt_pip_install())

        if config.arguments.verify_ntp:
            check_results['checks']['ntp_checks'].update(verify_ntp.get_service_status())

        if config.arguments.verify_lb:
            if verify_load_balancer.verify_dns_resolution(config.arguments.lb_fqdn):
                http_listener_threads = http_listener.start_listener_threads()
                logger.info('Sleeping for {} seconds to allow LB to see that we are live'.format(config.arguments.lb_delay_period))
                time.sleep(config.arguments.lb_delay_period)
                check_results['checks']['load_balancer_port_checks'].update(
                    verify_load_balancer.verify_port_connectivity(
                        config.arguments.k8s_port,
                        config.arguments.lb_fqdn
                    )
                )
                check_results['checks']['load_balancer_port_checks'].update(
                    verify_load_balancer.verify_port_connectivity(
                        config.arguments.web_port,
                        config.arguments.lb_fqdn
                    )
                )
                check_results['checks']['load_balancer_port_checks'].update(
                    verify_load_balancer.verify_port_connectivity(
                        config.arguments.spi_port,
                        config.arguments.lb_fqdn
                    )
                )

        logger.debug('Cleaning up temporary directory')
        shutil.rmtree(tmp_path)
        logger.debug(json.dumps(check_results, sort_keys=True, indent=4))

        table.print_table(check_results['checks'])

    if config.arguments.command == 'listener':
        logger.warning('not yet implemented')

if __name__ == "__main__":
    main()