# (C) Datadog, Inc. 2010-present
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)

from requests.exceptions import HTTPError

from datadog_checks.base import AgentCheck
from datadog_checks.openstack_controller.api.factory import make_api
from datadog_checks.openstack_controller.config import OpenstackConfig

HYPERVISOR_SERVICE_CHECK = {'up': AgentCheck.OK, 'down': AgentCheck.CRITICAL}

NOVA_HYPERVISOR_METRICS = [
    'current_workload',  # Available until version 2.87
    'disk_available_least',  # Available until version 2.87
    'free_disk_gb',  # Available until version 2.87
    'free_ram_mb',  # Available until version 2.87
    'local_gb',  # Available until version 2.87
    'local_gb_used',  # Available until version 2.87
    'memory_mb',  # Available until version 2.87
    'memory_mb_used',  # Available until version 2.87
    'running_vms',  # Available until version 2.87
    'vcpus',  # Available until version 2.87
    'vcpus_used',  # Available until version 2.87
    'load_1',
    'load_5',
    'load_15',
]

LEGACY_NOVA_HYPERVISOR_METRICS = [
    'current_workload',
    'disk_available_least',
    'free_disk_gb',
    'free_ram_mb',
    'local_gb',
    'local_gb_used',
    'memory_mb',
    'memory_mb_used',
    'running_vms',
    'vcpus',
    'vcpus_used',
]

LEGACY_NOVA_HYPERVISOR_LOAD_METRICS = {
    'load_1': 'hypervisor_load.1',
    'load_5': 'hypervisor_load.5',
    'load_15': 'hypervisor_load.15',
}


def _create_hypervisor_metric_tags(hypervisor_id, hypervisor_data, os_aggregates):
    tags = [
        f'hypervisor_id:{hypervisor_id}',
        f'hypervisor:{hypervisor_data.get("name")}',
        f'virt_type:{hypervisor_data.get("type")}',
        f'status:{hypervisor_data.get("status")}',
    ]
    for _os_aggregate_id, os_aggregate_value in os_aggregates.items():
        if hypervisor_data.get("name") in os_aggregate_value.get('hosts', []):
            tags.append('aggregate:{}'.format(os_aggregate_value.get("name")))
            tags.append('availability_zone:{}'.format(os_aggregate_value.get("availability_zone")))
    return tags


def _create_project_tags(project):
    return [f"project_id:{project.get('id')}", f"project_name:{project.get('name')}"]


class OpenStackControllerCheck(AgentCheck):
    def __init__(self, name, init_config, instances):
        super(OpenStackControllerCheck, self).__init__(name, init_config, instances)
        self.config = OpenstackConfig(self.log, self.instance)

    def check(self, _instance):
        self.log.debug(self.instance)
        try:
            api = make_api(self.config, self.log, self.http)
            api.create_connection()
            # Artificial metric introduced to distinguish between old and new openstack integrations
            self.gauge("openstack.controller", 1)
            self.service_check('openstack.keystone.api.up', AgentCheck.OK)
        except HTTPError as e:
            self.warning(e)
            self.log.error("HTTPError while creating api: %s", e)
            self.service_check('openstack.keystone.api.up', AgentCheck.CRITICAL, message=str(e))
            self.service_check('openstack.nova.api.up', AgentCheck.UNKNOWN)
            self.service_check('openstack.neutron.api.up', AgentCheck.UNKNOWN)
            self.service_check('openstack.ironic.api.up', AgentCheck.UNKNOWN)
            self.service_check('openstack.octavia.api.up', AgentCheck.UNKNOWN)
        except Exception as e:
            self.warning("Exception while creating api: %s", e)
            self.service_check('openstack.keystone.api.up', AgentCheck.CRITICAL)
            raise e
        else:
            self._report_metrics(api)

    def _report_metrics(self, api):
        projects = api.get_projects()
        self.log.debug("projects: %s", projects)
        for project in projects:
            self._report_project_metrics(api, project)

    def _report_project_metrics(self, api, project):
        self.log.debug("reporting metrics from project: [id:%s][name:%s]", project['id'], project['name'])
        project_tags = _create_project_tags(project)
        self._report_compute_metrics(api, project, project_tags)
        self._report_network_metrics(api, project)
        self._report_baremetal_metrics(api, project)
        self._report_load_balancer_metrics(api, project)

    def _report_compute_metrics(self, api, project, project_tags):
        project_id = project.get('id')
        response_time = api.get_compute_response_time(project_id)
        if response_time:
            self.service_check('openstack.nova.api.up', AgentCheck.OK)
            self.log.debug("response_time: %s", response_time)
            self.gauge('openstack.nova.response_time', response_time, tags=project_tags)
            compute_limits = api.get_compute_limits(project_id)
            self.log.debug("compute_limits: %s", compute_limits)
            for metric, value in compute_limits.items():
                self.gauge(f'openstack.nova.limits.{metric}', value, tags=project_tags)
            compute_quotas = api.get_compute_quota_set(project)
            self.log.debug("compute_quotas: %s", compute_quotas)
            for metric, value in compute_quotas.items():
                self.gauge(f'openstack.nova.quota_set.{metric}', value, tags=project_tags)
            compute_servers = api.get_compute_servers(project)
            self.log.debug("compute_servers: %s", compute_servers)
            for server_id, server_data in compute_servers.items():
                for metric, value in server_data['metrics'].items():
                    self.gauge(
                        f'openstack.nova.server.{metric}',
                        value,
                        tags=project_tags + [f'server_id:{server_id}', f'server_name:{server_data["name"]}'],
                    )
            compute_flavors = api.get_compute_flavors(project)
            self.log.debug("compute_flavors: %s", compute_flavors)
            for flavor_id, flavor_data in compute_flavors.items():
                for metric, value in flavor_data['metrics'].items():
                    self.gauge(
                        f'openstack.nova.flavor.{metric}',
                        value,
                        tags=project_tags + [f'flavor_id:{flavor_id}', f'flavor_name:{flavor_data["name"]}'],
                    )
            self._report_compute_hypervisors(api, project, project_tags)
        else:
            self.service_check('openstack.nova.api.up', AgentCheck.CRITICAL)

    def _report_compute_hypervisors(self, api, project, project_tags):
        compute_hypervisors_detail = api.get_compute_hypervisors_detail(
            project, self.instance.get('collect_hypervisor_load', True)
        )
        self.log.debug("compute_hypervisors_detail: %s", compute_hypervisors_detail)
        compute_os_aggregates = api.get_compute_os_aggregates(project['id'])
        self.log.debug("compute_os_aggregates: %s", compute_os_aggregates)
        for hypervisor_id, hypervisor_data in compute_hypervisors_detail.items():
            hypervisor_tags = project_tags + _create_hypervisor_metric_tags(
                hypervisor_id, hypervisor_data, compute_os_aggregates
            )
            self._report_hypervisor_service_check(
                hypervisor_data.get('state'), hypervisor_data["name"], hypervisor_tags
            )
            if self.instance.get('collect_hypervisor_metrics', True):
                self._report_hypervisor_metrics(hypervisor_id, hypervisor_data, hypervisor_tags)

    def _report_hypervisor_service_check(self, state, name, hypervisor_tags):
        self.service_check(
            'openstack.nova.hypervisor.up',
            HYPERVISOR_SERVICE_CHECK.get(state, AgentCheck.UNKNOWN),
            hostname=name,
            tags=hypervisor_tags,
        )

    def _report_hypervisor_metrics(self, hypervisor_id, hypervisor_data, hypervisor_tags):
        for metric, value in hypervisor_data.get('metrics', {}).items():
            self._report_hypervisor_metric(metric, value, hypervisor_tags)
            if self.instance.get('report_legacy_metrics', True):
                self._report_hypervisor_legacy_metric(metric, value, hypervisor_tags)

    def _report_hypervisor_metric(self, metric, value, tags):
        if metric in NOVA_HYPERVISOR_METRICS:
            self.gauge(f'openstack.nova.hypervisor.{metric}', value, tags=tags)

    def _report_hypervisor_legacy_metric(self, metric, value, tags):
        if metric in LEGACY_NOVA_HYPERVISOR_METRICS:
            self.gauge(f'openstack.nova.{metric}', value, tags=tags)
        elif metric in LEGACY_NOVA_HYPERVISOR_LOAD_METRICS:
            self.gauge(f'openstack.nova.{LEGACY_NOVA_HYPERVISOR_LOAD_METRICS[metric]}', value, tags=tags)

    def _report_network_metrics(self, api, project):
        tags = [f"project_id:{project['id']}", f"project_name:{project['name']}"]
        response_time = api.get_network_response_time(project)
        if response_time:
            self.service_check('openstack.neutron.api.up', AgentCheck.OK)
            self.log.debug("response_time: %s", response_time)
            self.gauge('openstack.neutron.response_time', response_time, tags=tags)
            network_quotas = api.get_network_quotas(project)
            self.log.debug("network_quotas: %s", network_quotas)
            for metric, value in network_quotas.items():
                self.gauge(f'openstack.neutron.quotas.{metric}', value, tags=tags)
        else:
            self.service_check('openstack.neutron.api.up', AgentCheck.CRITICAL)

    def _report_baremetal_metrics(self, api, project):
        tags = [f"project_id:{project['id']}", f"project_name:{project['name']}"]
        response_time = api.get_baremetal_response_time(project)
        if response_time:
            self.service_check('openstack.ironic.api.up', AgentCheck.OK)
            self.log.debug("response_time: %s", response_time)
            self.gauge('openstack.ironic.response_time', response_time, tags=tags)
        else:
            self.service_check('openstack.ironic.api.up', AgentCheck.CRITICAL)

    def _report_load_balancer_metrics(self, api, project):
        tags = [f"project_id:{project['id']}", f"project_name:{project['name']}"]
        response_time = api.get_load_balancer_response_time(project)
        if response_time:
            self.service_check('openstack.octavia.api.up', AgentCheck.OK)
            self.log.debug("response_time: %s", response_time)
            self.gauge('openstack.octavia.response_time', response_time, tags=tags)
        else:
            self.service_check('openstack.octavia.api.up', AgentCheck.CRITICAL)