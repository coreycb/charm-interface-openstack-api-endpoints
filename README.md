# Overview

This interface layer handles the communication with OpenStack Load Balancer
via the `openstack-api-endpoints` interface protocol.

# Usage

## Requires

The interface layer will set the following states, as appropriate:

  * `{relation_name}.connected`  The relation is established, but OpenStack
    Load Balancer has not been provided with the endpoint data.
  * `{relation_name}.available`  The OpenStack Load Balancer is ready for
    use. You can get the endpoint information via the following methods:
    * `frontend_ip(service_type)`
    * `frontend_port(service_type)`
    * `backend_ip(service_type)`
    * `backend_port(service_type)`
    * `backend_check_type(service_type)`

For example:

```python
from charmhelpers.core.hookenv import log, status_set, unit_get
from charms.reactive import when, when_not


@when('loadbalancer.connected')
def setup_loadbalancer(lb):
    lb.configure(service_type='nova',
                 frontend_port=8774,
                 backend_port=8764,
                 backend_ip=10.10.10.2,
                 check_type='http')
    lb.configure(service_type='nova-placement',
                 frontend_port=8778,
                 backend_port=8768,
                 backend_ip=10.10.10.2,
                 check_type='http')

@when('loadbalancer.available')
def use_loadbalancer(lb):
    log("nova-api endpoint data:")

    # data provided by our charm layer
    log("  check type     = %s" % lb.backend_check_type("nova-api"))
    log("  backend port   = %s" % lb.backend_port("nova-api"))
    log("  backend ip     = %s" % lb.backend_ip("nova-api"))
    log("  frontend port  = %s" % lb.frontend_port("nova-api"))

    # data provided by OpenStack Load Balancer
    log("  frontend ip    = %s\n" % lb.frontend_ip("nova-api"))

    log("nova-placement-api endpoint data:")

    # data provided by our charm layer
    log("  check type     = %s" % lb.backend_check_type("nova-placement-api"))
    log("  backend port   = %s" % lb.backend_port("nova-placement-api"))
    log("  backend ip     = %s" % lb.backend_ip("nova-placement-api"))
    log("  frontend port  = %s" % lb.frontend_port("nova-placement-api"))

    # data provided by OpenStack Load Balancer
    log("  frontend ip    = %s" % lb.frontend_ip("nova-placement-api"))

@when('loadbalancer.connected')
@when_not('loadbalancer.available')
def waiting_loadbalancer(lb):
    status_set('waiting', 'Waiting for OpenStack Load Balancer')

@when('loadbalancer.connected', 'loadbalancer.available')
def unit_ready(lb):
    status_set('active', 'Unit is ready')
```
