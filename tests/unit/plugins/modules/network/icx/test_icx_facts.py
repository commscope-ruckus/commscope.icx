# Copyright: (c) 2019, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.commscope.icx.tests.unit.compat.mock import patch
from ansible_collections.commscope.icx.plugins.modules import icx_facts
from ansible_collections.commscope.icx.tests.unit.plugins.modules.utils import set_module_args
from .icx_module import TestICXModule, load_fixture


class TestICXFactsModule(TestICXModule):

    module = icx_facts

    def setUp(self):
        super(TestICXFactsModule, self).setUp()
        self.mock_run_commands = patch('ansible_collections.commscope.icx.plugins.modules.icx_facts.run_commands')
        self.run_commands = self.mock_run_commands.start()

    def tearDown(self):
        super(TestICXFactsModule, self).tearDown()
        self.mock_run_commands.stop()

    def load_fixtures(self, commands=None):
        def load_from_file(*args, **kwargs):
            module = args
            commands = kwargs['commands']
            if(commands):
                resp = list()
                for cmd in commands:
                    fixtureName = cmd.replace(" ", "_")
                    newFixtureName = fixtureName.replace("_|_", "_")
                    output = load_fixture(newFixtureName).strip()
                    if(output):
                        resp.append(output)
                return resp
        self.run_commands.side_effect = load_from_file

    def test_icx_facts_default(self):
        set_module_args(dict(gather_subset=["default"]))
        result = self.execute_module()
        self.assertEqual(
            result['ansible_facts']['ansible_net_model'], 'Stackable ICX7150-C12-POE'
        )
        self.assertEqual(
            result['ansible_facts']['ansible_net_info'], 'Unit3:ICX7150-C12P, BSZ3242M003'
        )
        self.assertEqual(
            result['ansible_facts']['ansible_net_version'], '08.0.95'
        )
        self.assertEqual(
            result['ansible_facts']['ansible_net_hostname'], 'ruchusRouter148'
        )
        self.assertEqual(
            result['ansible_facts']['ansible_net_image'], 'SPR08095_b437.bin'
        )
        self.assertEqual(
            result['ansible_facts']['ansible_net_stacked_models'], ['ICX7150-24P-2X10G_2X1G', 'ICX7150-2X1GC', 'ICX7150-4X10GF',
                                                                    'ICX7150-48P-4X1G', 'ICX7150-2X1GC', 'ICX7150-4X10GF',
                                                                    'ICX7150-C12-2X1G', 'ICX7150-2X1GC', 'ICX7150-2X10GF']
        )

    def test_icx_facts_interfaces(self):
        set_module_args(dict(gather_subset=["interfaces"]))
        result = self.execute_module()

        self.assertEqual(
            result['ansible_facts']['ansible_net_interfaces']["GigabitEthernet1/1/1"]["macaddress"], "609c.9fe7.d600"
        )
        self.assertEqual(
            result['ansible_facts']['ansible_net_interfaces']["GigabitEthernet1/1/1"]["ipv4"]["address"], "192.168.1.1"
        )
        self.assertEqual(
            result['ansible_facts']['ansible_net_interfaces']["GigabitEthernet1/1/1"]["ipv4"]["subnet"], "24"
        )
        self.assertEqual(
            result['ansible_facts']['ansible_net_interfaces']["GigabitEthernet1/1/1"]["ipv4"]["subnet"], "24"
        )
        self.assertEqual(
            result['ansible_facts']['ansible_net_neighbors']["1/1/1"], [{'Port ID': '609c.9f31.afe0', 'System name': 'ICX7450-48 Router',
                                                                         'System description': 'Cisco IP Phone 9971, V1, sip9971.9-0-0-77',
                                                                         'Neighbor': '609c.9f31.afe0'}]
        )

    def test_icx_facts_hardware(self):
        set_module_args(dict(gather_subset=["hardware"]))
        result = self.execute_module()
        self.assertEqual(
            result['ansible_facts']['ansible_net_filesystems'], "flash"
        )
        self.assertEqual(
            result['ansible_facts']['ansible_net_filesystems_info'], {'flash': {'Stack unit 1': {'spacetotal': '2GiB', 'spacefree': '1287792Kb'}}}
        )
        self.assertEqual(
            result['ansible_facts']['ansible_net_memfree_kb']['Stack Unit1']['Free Memory'], '367152.0kb'
        )
        self.assertEqual(
            result['ansible_facts']['ansible_net_memtotal_kb']['Stack Unit1']['Total Memory'], '932320.0kb'
        )

    def test_icx_facts_not_hardware(self):
        set_module_args(dict(gather_subset=["!hardware"]))
        result = self.execute_module()

    def test_icx_facts_all(self):
        set_module_args(dict(gather_subset=["all"]))
        result = self.execute_module()
        self.assertEqual(
            result['ansible_facts']['ansible_net_filesystems'], "flash"
        )
        self.assertEqual(
            result['ansible_facts']['ansible_net_filesystems_info'], {'flash': {'Stack unit 1': {'spacetotal': '2GiB', 'spacefree': '1287792Kb'}}}
        )
        self.assertEqual(
            result['ansible_facts']['ansible_net_memfree_kb']['Stack Unit1']['Free Memory'], '367152.0kb'
        )
        self.assertEqual(
            result['ansible_facts']['ansible_net_memtotal_kb']['Stack Unit1']['Total Memory'], '932320.0kb'
        )
        self.assertEqual(
            result['ansible_facts']['ansible_net_interfaces']["GigabitEthernet1/1/1"]["macaddress"], "609c.9fe7.d600"
        )
        self.assertEqual(
            result['ansible_facts']['ansible_net_interfaces']["GigabitEthernet1/1/1"]["ipv4"]["address"], "192.168.1.1"
        )
        self.assertEqual(
            result['ansible_facts']['ansible_net_interfaces']["GigabitEthernet1/1/1"]["ipv4"]["subnet"], "24"
        )
        self.assertEqual(
            result['ansible_facts']['ansible_net_model'], 'Stackable ICX7150-C12-POE'
        )
        self.assertEqual(
            result['ansible_facts']['ansible_net_info'], 'Unit3:ICX7150-C12P, BSZ3242M003'
        )
        self.assertEqual(
            result['ansible_facts']['ansible_net_version'], '08.0.95'
        )
        self.assertEqual(
            result['ansible_facts']['ansible_net_hostname'], 'ruchusRouter148'
        )
        self.assertEqual(
            result['ansible_facts']['ansible_net_image'], 'SPR08095_b437.bin'
        )
        self.assertEqual(
            result['ansible_facts']['ansible_net_stacked_models'], ['ICX7150-24P-2X10G_2X1G', 'ICX7150-2X1GC', 'ICX7150-4X10GF',
                                                                    'ICX7150-48P-4X1G', 'ICX7150-2X1GC', 'ICX7150-4X10GF',
                                                                    'ICX7150-C12-2X1G', 'ICX7150-2X1GC', 'ICX7150-2X10GF']
        )
