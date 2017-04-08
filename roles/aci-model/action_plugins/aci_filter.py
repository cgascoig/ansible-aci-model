#!/usr/bin/python

import sys,os,inspect

# Add the path of this file to the python import path. I wonder if there's a better way to do this?
sys.path.append(os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0])))
from aci_model_plugin import ACIModelPlugin

class ActionModule(ACIModelPlugin):
	def run(self, tmp=None, task_vars=None, **kwargs):
		result = super(ActionModule, self).run(tmp, task_vars)

		module_args = result['invocation']['module_args']

		new_module_args = self._create_common_module_args(
			"uni/tn-%s/flt-%s"%(module_args['tenant_name'], module_args['filter_name']),
			module_args)

		new_module_args['body'] = self._create_mo('vzFilter',
			rn="flt-%s"%module_args['filter_name'],
			name=module_args['filter_name'],
			descr=module_args.get('description',''),
			)

		# add filter entries
		for flt in module_args['filter_entries']:
			vzEntry=self._create_mo('vzEntry', 
					rn="e-%s"%flt['name'], 
					etherT=flt.get('ether_type', 'unspecified'),
					prot=flt.get('proto', 'unspecified'),
					dFromPort=flt.get('dest_from_port', 'unspecified'),
					dToPort=flt.get('dest_to_port', 'unspecified'),
					sFromPort=flt.get('source_from_port', 'unspecified'),
					sToPort=flt.get('source_to_port', 'unspecified'),
					tcpRules=flt.get('tcp_rules', ''),
				)
			del vzEntry['vzEntry']['children']
			new_module_args['body']['vzFilter']['children'].append(vzEntry)


		return self._execute_module(module_name='aci_model', module_args=new_module_args, tmp=tmp, task_vars=task_vars)