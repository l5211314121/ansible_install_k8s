#!/usr/bin/env python

import json
from ansible.module_utils.common.collections import ImmutableDict
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
from ansible import context
from utils.utils import ParseResult

class ResultCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin
    """
    # def v2_runner_on_ok(self, result, **kwargs):
    #     """Print a json representation of the result
    #
    #     This method could store the result in an instance attribute for retrieval later
    #     """
    #     host = result._host
    #     print(json.dumps({host.name: result._result}, indent=4))

    def v2_runner_on_unreachable(self, result):
        # self.host_unreachable[result._host.get_name()] = result
        host = result._host
        print("==================")
        print(json.dumps({host.name: result._result}, indent=4))

    def v2_runner_on_ok(self, result, *args, **kwargs):
        # self.host_ok[result._host.get_name()] = result
        # host = result._host
        task_name = result._task._attributes['name']
        # action = result._task._attributes['action']
        if task_name == 'Gathering Facts':
            pass
        else:
            output = ParseResult.parse(result)
            print(output)

    def v2_runner_on_failed(self, result, *args, **kwargs):
        # self.host_failed[result._host.get_name()] = result
        host = result._host
        print("==================")
        print(json.dumps({host.name: result.__dict__}, indent=4))

# Instantiate our ResultCallback for handling results as they come in. Ansible expects this to be one of its main display outlets
results_callback = ResultCallback()

# since the API is constructed for CLI it expects certain options to always be set in the context object
context.CLIARGS = ImmutableDict(connection='ssh', module_path=['/usr/local/lib/python3.6/site-packages/ansible'], forks=10, become=None,
                                become_method=None, become_user=None, check=False, diff=False,
                                tags=[], syntax=False, start_at_task=None, verbosity=0
                                )

loader = DataLoader() # Takes care of finding and reading yaml, json and ini files
passwords = dict(vault_pass='secret')

# create inventory, use path to host config file as source or hosts in a comma separated string
inventory = InventoryManager(loader=loader, sources=['/etc/ansible/hosts'])

# variable manager takes care of merging all the different sources to give you a unified view of variables available in each context
variable_manager = VariableManager(loader=loader, inventory=inventory)

playbook = PlaybookExecutor(playbooks=['/root/packages/ansible_install_k8s/site.yml'],
                            inventory=inventory,
                            variable_manager=variable_manager,
                            loader=loader,
                            passwords=passwords)
# playbook._tqm._callback_plugins.append(results_callback)
playbook._tqm._callback_plugins = [results_callback]

playbook.run()