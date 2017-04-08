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
			"uni/tn-%s"%(module_args['tenant_name']),
			module_args)

		new_module_args['body'] = self._create_mo('fvTenant',
			name=module_args['tenant_name'])

		return self._execute_module(module_name='aci_model', module_args=new_module_args, tmp=tmp, task_vars=task_vars)