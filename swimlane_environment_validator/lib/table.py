#!/usr/bin/env python3
import os
import swimlane_environment_validator.lib.config as config
import swimlane_environment_validator.lib.log_handler as log_handler
import swimlane_environment_validator.lib.verify_load_balancer as verify_load_balancer

def print_table(checks):


    print("|{}|".format('-'*63))
    print("| {:^61} |".format('Environment Info'))
    print("|{}|".format('-'*63))
    print("| {:^15} | {:^30} | {:^10} |".format('Proxy Var','Message','Result'))
    print("|{}|".format('-'*63))    
    for key, value in checks['proxy_env_var_checks'].items():
        print("| {:15} | {:30} | {:10} |".format(key, value['message'], value['result']))
    print("|{}|".format('_'*63))

    print("")

    if config.arguments.verify_disk_space:
        print("|{}|".format('-'*83))
        print("| {:^81} |".format('Mount Info'))
        print("|{}|".format('-'*83))
        print("| {:^15} | {:^50} | {:^10} |".format('Directory', 'Message', 'Result'))    
        print("|{}|".format('-'*83))
        for key, value in checks['is_own_partition_checks'].items():
            print("| {:15} | {:50} | {:10} |".format(key, value['message'], value['result'] ))
        print("|{}|".format('_'*83))

        print("")

    if config.arguments.verify_disk_space:
        print("|{}|".format('-'*149))
        print("| {:^147} |".format('Directory Sizes'))
        print("|{}|".format('-'*149))
        print("| {:^15} | {:^20} | {:^20} | {:^70} | {:^10} |".format('Directory', 'Total Space Size', 'Percentage Free', 'Message', 'Result'))
        print("|{}|".format('-'*149))   
        for key, value in checks['directory_size_checks'].items():
            print("| {:15} | {:20} | {:20} | {:70} | {:10} |".format(key, str(value['Total Space Size']), str(value['Percentage Free']), str(value['message']), str(value['result']) ))
        print("|{}|".format('_'*149))

        print("")

    if config.arguments.verify_pip:
        print("|{}|".format('-'*101))
        print("| {:^99} |".format('Pip Checks'))
        print("|{}|".format('-'*101))
        print("| {:^50} | {:^10} |".format('Message', 'Results')) 
        print("|{}|".format('-'*51))   
        for key, value in checks['pip_checks'].items():
            print("| {:50} | {:10} |".format(str(value['message']), str(value['results'])))
        print("|{}|".format('_'*101))

        print("")

    if config.arguments.verify_ntp:
        print("|{}|".format('-'*51))
        print("| {:^49} |".format('Time Syncing Services'))
        print("|{}|".format('-'*51))
        print("| {:^10} | {:^10} | {:^10} | {:^10} |".format('Service', 'Installed', 'Enabled', 'Running')) 
        print("|{}|".format('-'*51))   
        for key, value in checks['ntp_checks'].items():
            print("| {:10} | {:10} | {:10} | {:10} |".format(key, str(value['installed']), str(value['enabled']), str(value['running'])))
        print("|{}|".format('_'*51))

        print("")

    if config.arguments.verify_public_endpoints and not config.arguments.offline:
        print("|{}|".format('-'*93))
        print("| {:^91} |".format('Public Endpoints'))
        print("|{}|".format('-'*93))
        print("| {:^60} | {:^15} | {:^10} |".format('Endpoint', 'Status Code', 'Result'))
        print("|{}|".format('-'*93))    
        for key, value in checks['public_endpoint_checks'].items():
            print("| {:60} | {:15} | {:10} |".format(key, str(value['status_code']), str(value['result'])))
        print("|{}|".format('_'*93))


    if config.arguments.verify_lb and verify_load_balancer.verify_dns_resolution(config.arguments.lb_fqdn):
        print("|{}|".format('-'*166))
        print("| {:^164} |".format('Load Balancer Endpoint'))
        print("|{}|".format('-'*166))
        print("| {:^50} | {:^80} | {:^15} | {:^10} |".format('Endpoint', 'Message', 'Status Code', 'Result'))
        print("|{}|".format('-'*166))    
        for key, value in checks['load_balancer_port_checks'].items():
            print("| {:50} | {:80} | {:15} | {:10} |".format(key, value['message'], str(value['status_code']), str(value['result'])))
        print("|{}|".format('_'*166))
