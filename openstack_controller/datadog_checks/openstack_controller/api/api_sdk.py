from datadog_checks.openstack_controller.api.api import Api


class ApiSdk(Api):
    def __init__(self, config, logger, http):
        pass

    def create_connection(self):
        pass  # pragma: no cover

    def get_projects(self):
        pass  # pragma: no cover

    def get_compute_response_time(self, project_id):
        pass  # pragma: no cover

    def get_compute_limits(self, project):
        pass  # pragma: no cover

    def get_compute_quota_set(self, project):
        pass  # pragma: no cover

    def get_compute_servers(self, project):
        pass  # pragma: no cover

    def get_compute_flavors(self, project):
        pass  # pragma: no cover

    def get_compute_hypervisors_detail(self, project, collect_hypervisor_load):
        pass  # pragma: no cover

    def get_compute_os_aggregates(self, project_id):
        pass  # pragma: no cover

    def get_network_response_time(self, project):
        pass  # pragma: no cover

    def get_network_quotas(self, project):
        pass  # pragma: no cover

    def get_baremetal_response_time(self, project):
        pass  # pragma: no cover