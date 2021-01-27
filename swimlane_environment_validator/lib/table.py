#!/usr/bin/env python3
import os
import swimlane_environment_validator.lib.config as config
import swimlane_environment_validator.lib.log_handler as log_handler
import swimlane_environment_validator.lib.verify_load_balancer as verify_load_balancer


def print_table(checks):


    print("|{}|".format('-'*80))
    print("|{:^80}|".format('Environment Info'))
    print("|{}|".format('-'*80))
    print("| {:^15} | {:^60} |".format('Proxy Var','Message'))
    print("|{}|".format('-'*80))    
    for key, value in checks['proxy_env_var_checks'].items():
        print("| {:15} | {:60} |".format(key, value['message']))
    print("|{}|".format('_'*80))

    print("")

    if config.arguments.verify_disk_space:
        print("|{}|".format('-'*79))
        print("|{:^79}|".format('Mount Info'))
        print("|{}|".format('-'*79))
        print("| {:^15} | {:^50} |{:^8}|".format('Directory', 'Message', 'Result'))    
        print("|{}|".format('-'*79))
        for key, value in checks['is_own_partition_checks'].items():
            print("| {:15} | {:50} | {:8} |".format(key, value['message'], value['result'] ))
        print("|{}|".format('_'*79))

        print("")

    if config.arguments.verify_disk_space:
        print("|{}|".format('-'*145))
        print("|{:^145}|".format('Directory Sizes'))
        print("|{}|".format('-'*145))
        print("| {:^15} | {:^20} | {:^20} | {:^70} |{:^8}|".format('Directory', 'Total Space Size', 'Percentage Used', 'Message', 'Result'))
        print("|{}|".format('-'*145))   
        for key, value in checks['directory_size_checks'].items():
            print("| {:15} | {:20} | {:20} | {:70} | {:8} |".format(key, str(value['Total Space Size']), str(value['Percentage Used']), str(value['message']), str(value['result']) ))
        print("|{}|".format('_'*145))

        print("")

    if config.arguments.verify_pip:
        print("|{}|".format('-'*86))
        print("|{:^86}|".format('Pip Checks'))
        print("|{}|".format('-'*86))
        print("| {:^75} |{:^8}|".format('Message', 'Result')) 
        print("|{}|".format('-'*86))   
        for key, value in checks['pip_checks'].items():
            print("| {:75} | {:8} |".format(str(value['message']), str(value['results'])))
        print("|{}|".format('_'*86))

        print("")

    if config.arguments.verify_ntp:
        print("|{}|".format('-'*51))
        print("|{:^51}|".format('Time Syncing Services'))
        print("|{}|".format('-'*51))
        print("| {:^10} | {:^10} | {:^10} | {:^10} |".format('Service', 'Installed', 'Enabled', 'Running')) 
        print("|{}|".format('-'*51))   
        for key, value in checks['ntp_checks'].items():
            print("| {:10} | {:10} | {:10} | {:10} |".format(key, str(value['installed']), str(value['enabled']), str(value['running'])))
        print("|{}|".format('_'*51))

        print("")

    if config.arguments.verify_executables:
        print("|{}|".format('-'*100))
        print("|{:^100}|".format('Disallowed Executables'))
        print("|{}|".format('-'*100))
        print("| {:^15} | {:^15} | {:^53} |{:^8}|".format('Executable', 'Path ','Message', 'Result'))    
        print("|{}|".format('-'*100))
        for key, value in checks['disallowed_executables'].items():
            print("| {:15} | {:15} | {:53} | {:8} |".format(key, value['path'], value['message'], value['result'] ))
        print("|{}|".format('_'*100))

        print("")

    if config.arguments.verify_public_endpoints and not config.arguments.offline:
        print("|{}|".format('-'*89))
        print("|{:^89}|".format('Public Endpoints'))
        print("|{}|".format('-'*89))
        print("| {:^60} | {:^15} |{:^8}|".format('Endpoint', 'Status Code', 'Result'))
        print("|{}|".format('-'*89))    
        for key, value in checks['public_endpoint_checks'].items():
            print("| {:60} | {:15} | {:8} |".format(key, str(value['status_code']), str(value['result'])))
        print("|{}|".format('_'*89))


    if config.arguments.verify_lb and verify_load_balancer.verify_dns_resolution(config.arguments.lb_fqdn):
        print("|{}|".format('-'*162))
        print("|{:^162}|".format('Load Balancer Endpoint'))
        print("|{}|".format('-'*162))
        print("| {:^50} | {:^80} | {:^15} |{:^8}|".format('Endpoint', 'Message', 'Status Code', 'Result'))
        print("|{}|".format('-'*162))    
        for key, value in checks['load_balancer_port_checks'].items():
            print("| {:50} | {:80} | {:15} | {:8} |".format(key, value['message'], str(value['status_code']), str(value['result'])))
        print("|{}|".format('_'*162))

    print("|{}|".format('-'*150))
    print("|{:^150}|".format('!!! Additional Manual Checks !!!'))
    print("|{:^150}|".format('Each SPI Node must have a unique hostname as determined by hostnamectl.'))
    print("|{:^150}|".format('Each SPI Node should have DNS-resolvable hostnames.'))
    print("|{:^150}|".format('Each SPI Node must have reliable and consistent time. An NTP daemon is recommended.'))
    print("|{}|".format('_'*150))