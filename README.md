# swimlane-environment-validator

This binary will run through various checks for the Swimlane Platform Installer.

It is designed to be ran by the customer in order to verify their environment before engaging PS for the install.

This script if highly configurable with various options to skip checks. Most checks are enabled by default. See `swimlane-environment-validator verify --help` for more information.

## How to use

Download and extract the binary, and make it executable.

Add a single node to your load balancer to ensure the other nodes do not interfere with testing.

From this node, run the executable:
```
$ ./swimlane-environment-validator verify --lb-fqdn <loadbalancer address>
```

## Verify subcommand arguments:
```
$ ./swimlane-environment-validator verify --help
usage: __main__ verify [-h] [--verify-lb VERIFY_LB] [--lb-fqdn LB_FQDN]
                       [--lb-delay-period LB_DELAY_PERIOD]
                       [--additional-node-fqdn ADDITIONAL_NODE_FQDN]
                       [--offline OFFLINE]
                       [--verify-public-endpoints VERIFY_PUBLIC_ENDPOINTS]
                       [--verify-pip VERIFY_PIP] [--verify-ntp VERIFY_NTP]
                       [--pip-config PIP_CONFIG]
                       [--verify-swimlane-tls-certificate VERIFY_SWIMLANE_TLS_CERTIFICATE]
                       [--swimlane-certificate SWIMLANE_CERTIFICATE]
                       [--swimlane-key SWIMLANE_KEY]
                       [--verify-disk-space VERIFY_DISK_SPACE]

optional arguments:
  -h, --help            show this help message and exit
  --verify-lb VERIFY_LB
                        Load Balancer FQDN. Default is the hostname of the
                        node running the verifier script.
  --lb-fqdn LB_FQDN     Load Balancer FQDN. Default is the hostname of the
                        node running the verifier script.
  --lb-delay-period LB_DELAY_PERIOD
                        Time in seconds to wait for before testing the load
                        balancer. Allows the LB to see that there is something
                        listening. Default 90s.
  --additional-node-fqdn ADDITIONAL_NODE_FQDN
                        Node FQDNs. May be specified multiple times for
                        multiple nodes. Default is the current hosts' FQDN.
  --offline OFFLINE     Run in Offline mode
  --verify-public-endpoints VERIFY_PUBLIC_ENDPOINTS
                        Run checks against public endpoints to verify
                        accessibility.
  --verify-pip VERIFY_PIP
                        Test connectivity to PyPi. Requires pip and virtualenv
                        to be installed.
  --verify-ntp VERIFY_NTP
                        Verify that ntp is enabled and running.
  --pip-config PIP_CONFIG
                        Test connectivity to PyPi using the specified pip
                        config. Requires pip and virtualenv to be installed.
  --verify-swimlane-tls-certificate VERIFY_SWIMLANE_TLS_CERTIFICATE
                        Test connectivity to PyPi using the specified pip
                        config. Requires pip and virtualenv to be installed.
  --swimlane-certificate SWIMLANE_CERTIFICATE
                        File path for the TLS Certificate for Swimlane
  --swimlane-key SWIMLANE_KEY
                        File path for the TLS Certificate Key for Swimlane
  --verify-disk-space VERIFY_DISK_SPACE
                        Enable verification of disk space and partitions
```

## Listener subcommand:

Sometimes for debugging your load balancer it is useful to have a daemon that listens on the ports that the SPI needs for communication.

The listener will run on port 6443, 8800, and 443 (if ran as root) until the user presses the enter key to exit:

```
$ ./swimlane-environment-validator listener
```

The addresses that are listened for can be changed via these optional arguments:

```
optional arguments:
  -h, --help            show this help message and exit
  --k8s-port K8S_PORT   Port to listen for the Kubernetes Load Balancer check.
                        Default is 6443.
  --web-port WEB_PORT   Port to listen for the HTTPS Load Balancer check.
                        Default is 443.
  --spi-port SPI_PORT   Port to listen for the Swimlane Platform Installer
                        Load Balancer check. Default is 8800.
```


## Known Issues:
* https://storage.googleapis.com always fails the endpoint test with 400. Until we discover an endpoint that allows unauthenticated GET requests, it will remain this way.
* https://production.cloudflare.docker.com always returns a 403 status code. Until we discover an endpoint that allows unauthenticated GET requests, it will remain this way.
* The verify-pip check requires outside binaries, python3 and venv.

`swimlane-environment-validator` is a [Swimlane](https://swimlane.com) open-source project; we believe in giving back to the open-source community by sharing some of the projects we build for our application. Swimlane is an automated cyber security operations and incident response platform that enables cyber security teams to leverage threat intelligence, speed up incident response and automate security operations.
