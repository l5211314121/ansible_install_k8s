import json
import shutil
from ansible.module_utils.common.collections import ImmutableDict
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
from ansible import context
import ansible.constants as C
from ansible.executor.playbook_executor import PlaybookExecutor

class ResultCallback(CallbackBase):

    def v2_runner_on_ok(self, result, **kwargs):
        host = result._host
        print(json.dumps({host.name: result._result}, indent=4))

    def v2_runner_on_failed(self, result, ignore_errors=False):
        host = result._host
        print(json.dumps({host.name: result._result}, indent=4))

    def v2_runner_on_unreachable(self, result):
        host = result._host
        print(json.dumps({host.name: result._result}, indent=4))

def test_ansible():
    # module_path='/home/developer/test/env/lib/python3.7/site-packages/ansible'
    context.CLIARGS = ImmutableDict(connection='ssh', module_path=['/root/'], forks=10, become=None,
                                    become_method=None, become_user=None, check=False, diff=False, syntax=False,
                                    start_at_task=None, tags=['api_test'])
    results_callback = ResultCallback()
    loader = DataLoader()
    inventory = InventoryManager(loader=loader, sources=['/etc/ansible/hosts'])
    variable_manager = VariableManager(loader=loader, inventory=inventory)
    passwords = {}
    playbook_path = '/root/playbook/site.yml'
    pbex = PlaybookExecutor(playbooks=[playbook_path], inventory=inventory, variable_manager=variable_manager, loader=loader, passwords=passwords)

    results = pbex.run()
    print results
test_ansible()