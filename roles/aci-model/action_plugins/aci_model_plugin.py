#!/usr/bin/python

from ansible.plugins.action import ActionBase

class ACIModelPlugin(ActionBase):
	def _create_mo(self, cls, children=[], **kwargs):
		obj = {cls: {
			'attributes': kwargs,
			'children': children
		}}

		return obj
	def _create_common_module_args(self, dn, module_args):
		# TODO: add provider option

		new_module_args = {}

		if 'provider' in module_args:
			prov = module_args['provider']
			new_module_args['username'] = prov.get('username')
			new_module_args['password'] = prov.get('password')
			new_module_args['url'] = prov.get('url')

		if 'username' in module_args:
			new_module_args['username'] = module_args['username']
		if 'password' in module_args:
			new_module_args['password'] = module_args['password']
		if 'url' in module_args:
			new_module_args['url'] = module_args['url']
	
		new_module_args['dn'] = dn


		return new_module_args

	def _add_child(self, mo, child):
		mo[mo.keys()[0]]['children'].append(child)