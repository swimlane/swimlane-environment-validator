#!/usr/bin/env python3
import os
import sys
import argparse
import socket
import yaml

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

parser = argparse.ArgumentParser()
commands = parser.add_subparsers(dest='command')

version_action = commands.add_parser('version', help="Print the version and then exit.")

parser.add_argument("--k8s-port", type=int,  default=6443,
                        help="Port to listen for the Kubernetes Load Balancer check. Default is 6443.")
parser.add_argument("--web-port", type=int, default=443,
                        help="Port to listen for the HTTPS Load Balancer check. Default is 443.")
parser.add_argument("--spi-port", type=int, default=8800,
                        help="Port to listen for the Swimlane Platform Installer Load Balancer check. Default is 8800.")
parser.add_argument("--debug", type=str2bool, default=False,
                        help="Set to True to enable debug mode.")
parser.add_argument("--use-color", type=str2bool, default=True,
                        help="Enable or Disable ANSI color codes. Useful for CI or non-interactive terminals.")

verify_action = commands.add_parser('verify', help="Run the environment verifier.")

verify_action.add_argument("--verify-lb", type=str2bool, default=True,
                        help="Load Balancer FQDN. Default is the hostname of the node running the verifier script.")

verify_action.add_argument("--enable-listeners", type=str2bool, default=True,
                        help="Enable listeners if your load balancer has no healthy nodes.")

verify_action.add_argument("--lb-fqdn", type=str, default=socket.gethostname(),
                        help="Load Balancer FQDN. Default is the hostname of the node running the verifier script.")

verify_action.add_argument("--lb-delay-period", type=int, default=90,
                        help="Time in seconds to wait for before testing the load balancer. Allows the LB to see that there is something listening. Default 90s.")

verify_action.add_argument("--offline", type=str2bool, default=False,
                        help="Run in Offline mode.")

verify_action.add_argument("--verify-public-endpoints", type=str2bool, default=True,
                        help="Run checks against public endpoints to verify accessibility.")

verify_action.add_argument("--verify-executables", type=str2bool, default=True,
                        help="Verify if any disallowed executables are installed.")

verify_action.add_argument("--verify-pip", type=str2bool, default=False,
                        help="Test connectivity to PyPi. Requires pip and virtualenv to be installed.")

verify_action.add_argument("--verify-ntp", type=str2bool, default=True,
                        help="Verify that ntp is enabled and running.")

verify_action.add_argument("--pip-config", type=str, default=False,
                        help="Test connectivity to PyPi using the specified pip config. Requires pip and virtualenv to be installed.")

verify_action.add_argument("--verify-swimlane-tls-certificate", type=str, default=False,
                        help="Check attributes of the provided tls certificate for validity.")

verify_action.add_argument("--swimlane-certificate", type=str, default=False,
                        help="File path for the TLS Certificate for Swimlane.")
verify_action.add_argument("--swimlane-key", type=str, default=False,
                        help="File path for the TLS Certificate Key for Swimlane.")

verify_action.add_argument("--verify-disk-space", type=str2bool, default=True,
                        help="Enable verification of disk space and partitions.")

verify_action.add_argument("--verify-intra-cluster-ports", type=str2bool, default=False,
                        help="Enable verification of communication between nodes. Requires --additional-node-fqdn.")

verify_action.add_argument("--additional-node-fqdn", action='append',
                        help="Node FQDNs. May be specified multiple times for multiple nodes.")

verify_action.add_argument("--installer-patch", type=str, default=False,
                        help="Validate and use an installer patch file. Supply the same file that you will provide to the `install-spec-file` argument of the installer script.")

verify_action.add_argument("--proxy-override", type=str, default=False,
                        help="This string will override the proxy string if one is supplied in the install-spec-file.")


listener_action = commands.add_parser('listener', help="Load Balancer Listener daemon.")
listener_action.add_argument("--lb-fqdn", type=str, default=socket.gethostname(),
                        help="Load Balancer FQDN. Default is the hostname of the node running the verifier script.")

arguments = parser.parse_args()

if arguments.command == 'version':
    from .. import __version__
    print(__version__.__version__)
    sys.exit(0)

if arguments.command is None:
    parser.print_help()
    sys.exit(1)

if arguments.use_color:
    #Terminal ANSI color codes
    OK = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
else:
    OK = ''
    WARNING = ''
    FAIL = ''
    ENDC = ''

LB_CONNECTIVITY_PORTS = [
    arguments.k8s_port,
    arguments.web_port,
    arguments.spi_port,
    4443
]

INTRA_CLUSTER_PORTS = [
    2379,
    2380,
    6783,
    6784,
    10250,
    10251,
    10252,
    32000, # Randomly chosen ports in the
    32100, # 32,000 - 32,767 range
    32500,
    32767
]

if arguments.command == 'verify':

    installer_yaml = False
    if arguments.installer_patch:
        try:
            with open(arguments.installer_patch, 'r') as stream:        
                installer_yaml = yaml.load(stream)
        except:
            print('Unable to parse {}, is this valid yaml?'.format(arguments.installer_patch))
            sys.exit(1)

    PUBLIC_ENDPOINTS = [
        { "endpoint": "https://get.swimlane.io/nginx-health", "status_code": 200 },
        { "endpoint": "https://k8s.kurl.sh", "status_code": 200 },
        { "endpoint": "https://kurl.sh", "status_code": 200 },
        { "endpoint": "https://kurl-sh.s3.amazonaws.com/dist/ekco-0.6.0.tar.gz", "status_code": 200 },
        { "endpoint": "https://registry.replicated.com/v2", "status_code": 301 },
        { "endpoint": "https://proxy.replicated.com/healthz", "status_code": 200 },
        { "endpoint": "https://k8s.gcr.io", "status_code": 302 },
        { "endpoint": "https://storage.googleapis.com", "status_code": 400 },
        { "endpoint": "https://quay.io", "status_code": 200 },
        { "endpoint": "https://replicated.app", "status_code": 200 },
        { "endpoint": "https://auth.docker.io/token", "status_code": 200 },
        { "endpoint": "https://registry-1.docker.io", "status_code": 404 },
        { "endpoint": "https://production.cloudflare.docker.com", "status_code": 403 },
        { "endpoint": "https://files.pythonhosted.org", "status_code": 200 },
        { "endpoint": "https://pypi.org", "status_code": 200 }
    ]

    NTP_EXECUTABLES = [
        "ntpd",
        "chronyd",
        "systemd-timesyncd.service"
    ]

    UNALLOWED_EXECUTABLES = [
        "docker",
        "ctr",
        "containerd",
        "kubelet"
    ]

    lb_scheme = "https"
    LB_CONNECTIVITY_ENDPOINTS = [
        '{}://{}:{}/livez'.format(lb_scheme, arguments.lb_fqdn, arguments.k8s_port),
        '{}://{}:{}/nginx-health'.format(lb_scheme, arguments.lb_fqdn, arguments.web_port),
        '{}://{}:{}/healthz'.format(lb_scheme, arguments.lb_fqdn, arguments.spi_port)
    ]

    # Directory name, minimum space in bytes. Subtract one GB so that a 400GB raw disk is acceptable
    DIRECTORY_SIZES_CHECK = {
        "/var/openebs": "300G",
        "/var/lib/docker": "100G",
        "/var/lib/kubelet": "100G",
        "/var/lib/kurl": "10G",
        "/opt": "50G",
        "/": "50G"
    }

    DIRECTORY_IS_MOUNT_CHECK = [
        "/var/openebs",
        "/var/lib/docker",
        "/var/lib/kubelet",
        "/opt"
    ]

if arguments.command == 'listener':
    pass
