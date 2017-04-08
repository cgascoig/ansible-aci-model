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
			"uni/tn-%s/brc-%s"%(module_args['tenant_name'], module_args['contract_name']),
			module_args)

		new_module_args['body'] = self._create_mo('vzBrCP',
			rn="brc-%s"%module_args['contract_name'],
			name=module_args['contract_name'],
			descr=module_args.get('description',''),
			children=[
				self._create_mo('vzSubj',
					rn='subj-ansible_subj',
					name='ansible_subj',
					revFltPorts='yes'
				)
			]
			)

		# add filters
		for flt in module_args['filter_name_list']:
			vzRsSubjFiltAtt=self._create_mo('vzRsSubjFiltAtt', 
					rn="rssubjFiltAtt-%s"%flt, 
					tnVzFilterName=flt,
					children=[]
				)
			new_module_args['body']['vzBrCP']['children'][0]['vzSubj']['children'].append(vzRsSubjFiltAtt)

		return self._execute_module(module_name='aci_model', module_args=new_module_args, tmp=tmp, task_vars=task_vars)