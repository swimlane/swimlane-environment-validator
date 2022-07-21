# swimlane-environment-validator

This binary will run through various checks for the Swimlane Platform Installer.

It is designed to be ran by the customer in order to verify their environment before engaging PS for the install.

This script if highly configurable with various options to skip checks. Most checks are enabled by default. See `swimlane-environment-validator verify --help` for more information.

## How to use

If preparing for a new Swimlane installation.

For CentOS / Red Hat:
```
yum -y install centos-release-scl wget
yum -y install rh-python36
scl enable rh-python36 bash
```

For Ubuntu:
```
apt -y install build-essential libssl-dev libffi-dev python-dev
apt -y install python3-pip
pip install virtualenv
```

And finally, for either Ubuntu or CentOS / Red Hat:
```
wget https://github.com/swimlane/swimlane-environment-validator/releases/download/0.5.3/swimlane-environment-validator
chmod +x ./swimlane-environment-validator
./swimlane-environment-validator verify
```

General Use:
Download and extract the binary, and make it executable.

Add a single node to your load balancer to ensure the other nodes do not interfere with testing.

From this node, run the executable:
```
$ ./swimlane-environment-validator verify --lb-fqdn <loadbalancer address>
```

For offline install there is an `--offline` flag that will disable any online checks.


## Known Issues:
* The verify-pip check requires outside binaries, python3 and venv.
* On some operating systems, the script will fail with `error while loading shared libraries: libz.so.1: failed to map segment from shared object: Operation not permitted`. This occur usually if you are running the script as root and the `/tmp` directory is mounted with `noexec`. To work around this, you can either run the script as a non-root user, or you can set the `TMPDIR` environment variable to a writable and executable directory.

`swimlane-environment-validator` is a [Swimlane](https://swimlane.com) open-source project; we believe in giving back to the open-source community by sharing some of the projects we build for our application. Swimlane is an automated cyber security operations and incident response platform that enables cyber security teams to leverage threat intelligence, speed up incident response and automate security operations.
