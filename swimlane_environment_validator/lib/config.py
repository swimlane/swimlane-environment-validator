#!/usr/bin/env python3
import os
import argparse
import socket

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

verify_action.add_argument("--verify-pip", type=str2bool, default=True,
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

listener_action = commands.add_parser('listener', help="Load Balancer Listener daemon.")
listener_action.add_argument("--lb-fqdn", type=str, default=socket.gethostname(),
                        help="Load Balancer FQDN. Default is the hostname of the node running the verifier script.")

arguments = parser.parse_args()

if arguments.command == 'version':
    import sys
    from .. import __version__
    print(__version__.__version__)
    sys.exit(0)

PUBLIC_ENDPOINTS = [
    "https://get.swimlane.io/nginx-health",
    "https://k8s.kurl.sh",
    "https://kurl.sh",
    "https://kurl-sh.s3.amazonaws.com/dist/ekco-0.6.0.tar.gz",
    "https://registry.replicated.com/v2",
    "https://proxy.replicated.com/healthz",
    "https://k8s.gcr.io",
    "https://storage.googleapis.com",
    "https://quay.io",
    "https://replicated.app",
    "https://auth.docker.io/token",
    "https://registry-1.docker.io",
    "https://production.cloudflare.docker.com",
    "https://files.pythonhosted.org",
    "https://pypi.org"
]

NTP_EXECUTABLES = [
    "ntpd",
    "chronyd"
]

UNALLOWED_EXECUTABLES = [
    "docker",
    "ctr",
    "containerd",
    "kubelet"
]

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

try:
    if arguments.enable_listeners:
        enabled_listeners = True
except AttributeError:
    enabled_listeners = False

if enabled_listeners:
    LB_CONNECTIVITY_ENDPOINTS = [
        'http://{}:{}/health'.format(arguments.lb_fqdn, arguments.k8s_port),
        'http://{}:{}/health'.format(arguments.lb_fqdn, arguments.web_port),
        'http://{}:{}/health'.format(arguments.lb_fqdn, arguments.spi_port)
    ]
else:
    LB_CONNECTIVITY_ENDPOINTS = [
        'https://{}:{}/livez'.format(arguments.lb_fqdn, arguments.k8s_port),
        'https://{}:{}/nginx-health'.format(arguments.lb_fqdn, arguments.web_port),
        'https://{}:{}/healthz'.format(arguments.lb_fqdn, arguments.spi_port)
    ]

LB_CONNECTIVITY_PORTS = [
    arguments.k8s_port,
    arguments.web_port,
    arguments.spi_port
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

# Directory name, minimum space in bytes. Subtract one GB so that a 400GB raw disk is acceptable
DIRECTORY_SIZES_CHECK = {
    "/var/openebs": "300G",
    "/var/lib/docker": "100G",
    "/opt": "50G",
    "/": "50G"
}

DIRECTORY_IS_MOUNT_CHECK = [
    "/var/openebs",
    "/var/lib/docker",
    "/opt"
]
