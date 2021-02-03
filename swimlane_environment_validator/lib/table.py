#!/usr/bin/env python3
import os
from prettytable import PrettyTable
import swimlane_environment_validator.lib.config as config
import swimlane_environment_validator.lib.log_handler as log_handler
import swimlane_environment_validator.lib.verify_load_balancer as verify_load_balancer

def print_table(checks):

    x = PrettyTable()
    x.title = 'Environment Info'
    x.field_names = ['Proxy Var','Message']
    for k,v in checks['proxy_env_var_checks'].items():
        row = [*v.values()]
        x.add_row(row)
    print(x.get_string())

    if config.arguments.verify_disk_space:
        x = PrettyTable()
        x.title = 'Mount Info'
        x.field_names = ['Directory', 'Message', 'Result']
        for k,v in checks['is_own_partition_checks'].items():
            row = [*v.values()]
            row.insert(0,k)
            x.add_row(row)
        print(x.get_string())

    if config.arguments.verify_disk_space:
        x = PrettyTable()
        x.title = 'Directory Sizes'
        x.field_names = ['Directory', 'Total Space Size', 'Percentage Used', 'Message', 'Result']
        for k,v in checks['directory_size_checks'].items():
            row = [*v.values()]
            row.insert(0,k)
            x.add_row(row)
        print(x.get_string())

    if config.arguments.verify_pip:
        x = PrettyTable()
        x.title = 'Pip Checks'
        x.field_names = ['Message', 'Result']
        for k,v in checks['pip_checks'].items():
            row = [*v.values()]
            x.add_row(row)
        print(x.get_string())

    if config.arguments.verify_ntp:
        x = PrettyTable()
        x.title = 'Time Syncing Services'
        x.field_names = ['Service', 'Running', 'Enabled']
        for k,v in checks['ntp_checks'].items():
            row = [*v.values()]
            row.insert(0,k)
            x.add_row(row)
        print(x.get_string())

    if config.arguments.verify_executables:
        x = PrettyTable()
        x.title = 'Disallowed Executables'
        x.field_names = ['Executable', 'Path ','Message', 'Result']
        for k,v in checks['disallowed_executables'].items():
            row = [*v.values()]
            row.insert(0,k)
            x.add_row(row)
        print(x.get_string())

    if config.arguments.verify_public_endpoints and not config.arguments.offline:
        x = PrettyTable()
        x.title = 'Public Endpoints'
        x.field_names = ['Endpoint', 'Status Code', 'Result']
        for k,v in checks['public_endpoint_checks'].items():
            row = [*v.values()]
            row.insert(0,k)
            x.add_row(row)
        print(x.get_string())

    if config.arguments.verify_lb and verify_load_balancer.verify_dns_resolution(config.arguments.lb_fqdn):
        x = PrettyTable()
        x.title = 'Load Balancer Endpoints'
        x.field_names = ['Endpoint', 'Result']
        for k,v in checks['load_balancer_port_checks'].items():
            row = [*v.values()]
            row.insert(0,k)
            x.add_row(row)
        print(x.get_string())

    if config.arguments.verify_swimlane_tls_certificate:
        x = PrettyTable()
        x.title = 'Certificate Validity'
        x.field_names = ['Certificate', 'Expiration', 'Message', 'Result']
        for k,v in checks['swimlane_certificate_checks'].items():
            row = [*v.values()]
            row.insert(0,k)
            x.add_row(row)
        print(x.get_string())

    if config.arguments.verify_intra_cluster_ports and config.arguments.additional_node_fqdn:
        field_names = config.INTRA_CLUSTER_PORTS
        field_names.insert(0,'Node')
        x = PrettyTable()
        x.title = 'Intra-Cluster Communication'
        x.field_names = field_names
        for k,v in checks['intra_port_connectivity'].items():
            row = [*v.values()]
            row.insert(0,k)
            x.add_row(row)
        print(x.get_string())

    print("|{}|".format('-'*141))
    print("|{:^150}|".format('{}!!! Additional Manual Checks !!!{}'.format(config.WARNING, config.ENDC)))
    print("|{:^150}|".format('{}Each SPI Node must have a unique hostname as determined by hostnamectl.{}'.format(config.WARNING, config.ENDC)))
    print("|{:^150}|".format('{}Each SPI Node should have DNS-resolvable hostnames.{}'.format(config.WARNING, config.ENDC)))
    print("|{:^150}|".format('{}Each SPI Node must have reliable and consistent time. An NTP daemon is recommended.{}'.format(config.WARNING, config.ENDC)))
    print("|{}|".format('_'*141))
