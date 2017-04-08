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
			"uni/tn-%s/ap-%s/epg-%s"%(module_args['tenant_name'], module_args['ap_name'], module_args['epg_name']),
			module_args)

		new_module_args['body'] = self._create_mo('fvAEPg',
			rn="epg-%s"%module_args['epg_name'],
			name=module_args['epg_name'],
			descr=module_args['description'],
			children = [
				self._create_mo('fvRsBd', rn='rsbd', tnFvBDName=module_args['bd_name'])
			]
			)

		# add domain attachments
		for domain_dn in module_args['domain_dn_list']:
			new_module_args['body']['fvAEPg']['children'].append(
				self._create_mo('fvRsDomAtt', rn="rsdomAtt-[%s]"%domain_dn, tDn=domain_dn)
			)

		for cons in module_args['consumed_list']:
			self._add_child(new_module_args['body'],
				self._create_mo('fvRsCons', rn="rscons-%s"%cons, tnVzBrCPName=cons))

		for prov in module_args['provided_list']:
			self._add_child(new_module_args['body'],
				self._create_mo('fvRsProv', rn="rsprov-%s"%prov, tnVzBrCPName=prov))

		return self._execute_module(module_name='aci_model', module_args=new_module_args, tmp=tmp, task_vars=task_vars)