from charmhelpers.core import hookenv
from charms.reactive import RelationBase
from charms.reactive import hook
from charms.reactive import scopes


class OpenStackLoadBalancerRequires(RelationBase):
    scope = scopes.GLOBAL

    @hook('{requires:openstack-api-endpoints}-relation-joined')
    def joined(self):
        self.set_state('{relation_name}.connected')

    @hook('{requires:openstack-api-endpoints}-relation-changed')
    def changed(self):
        if self.data_complete():
            self.set_state('{relation_name}.available')

    @hook('{requires:openstack-api-endpoints}-relation-{broken,departed}')
    def departed(self):
        self.remove_state('{relation_name}.connected')
        self.remove_state('{relation_name}.available')

    def configure(self, service_type, frontend_port, backend_port, backend_ip,
                  check_type):
        """
        Called by charm layer that uses this interface to configure an endpoint
        """
        relation_info = {
            service_type + '_service_type': service_type,
            service_type + '_frontend_port': frontend_port,
            service_type + '_backend_ip': backend_ip,
            service_type + '_backend_port': backend_port,
            service_type + '_backend_check_type': backend_check_type,
        }
        self.set_service_type(service_type)
        self.set_remote(**relation_info)
        self.set_local(**relation_info)

    def set_service_type(self, service_type):
        """
        Store all of the endpoint service_types in a list.
        """
        service_types = self.get_local('service_types')
        if service_types:
            if service_type not in service_types:
                self.set_local('service_types', service_types + [service_type])
        else:
            self.set_local('service_types', [service_type])

    def get_service_types(self):
        """
        Return the list of saved service_types.
        """
        return self.get_local('service_types')

    def frontend_ip(self, service_type):
        """
        Return a frontend ip for a configured endpoint.
        """
        return self.get_remote(service_type + '_frontend_ip')

    def frontend_port(self, service_type):
        """
        Return a frontend port for a configured endpoint.
        """
        return self.get_local(service_type + '_frontend_port')

    def backend_ip(self, service_type):
        """
        Return a backend ip for a configured endpoint.
        """
        return self.get_local(service_type + '_backend_ip')

    def backend_port(self, service_type):
        """
        Return a backend port for a configured endpoint.
        """
        return self.get_local(service_type + '_backend_port')

    def backend_check_type(self, service_type):
        """
        Return a backend check type for a configured endpoint.
        """
        return self.get_local(service_type + '_backend_check_type')

    def data_complete(self):
        """
        Check if required data is complete.
        """
        data = {}
        for service_type in self.get_service_types():
            key = service_type + '_frontend_ip'
            data[key] = self.get_remote(key)
        if data and all(data.values()):
            return True
        return False
