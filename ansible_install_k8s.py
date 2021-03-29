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
    def __init__(self, *args, **kwargs):
        super(ResultCallback, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

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
    module_path='/usr/local/lib/python3.6/site-packages/ansible'
    context.CLIARGS = ImmutableDict(connection='ssh', module_path=['/root/', module_path], forks=10, become=None,
                                    become_method=None, become_user=None, check=False, diff=False, syntax=False,
                                    start_at_task=None, tags=[], verbosity=2)
    results_callback = ResultCallback()
    loader = DataLoader()
    inventory = InventoryManager(loader=loader, sources=['/etc/ansible/hosts'])
    variable_manager = VariableManager(loader=loader, inventory=inventory)
    passwords = {}
    playbook_path = '/root/Projects/playbooks/ansible_install_k8s/site.yml'
    pbex = PlaybookExecutor(playbooks=[playbook_path], inventory=inventory, variable_manager=variable_manager, loader=loader, passwords=passwords)
    # pbex._tqm._stdout_callback = results_callback
    results = pbex.run()
    print (results)

test_ansible()