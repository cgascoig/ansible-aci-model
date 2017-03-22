# ansible-aci-model
Ansible module and roles to declaratively define Cisco ACI policy model 

## Requirements
- Ansible (tested with 2.2.1.0)
- requests module (tested with 2.8.1)

## Usage
### aci_model module
The aci_model module (located in the aci-model role) allows the specification of a base distinguished name (DN) and desired model. For example, the following specifies that there should be an application profile named test-ap under the tenant ACILab:
```yaml
tasks:
      - name: test aci_model
        aci_model:
          username: "{{ username }}"
          password: "{{ password }}"
          url: "http://{{ inventory_hostname }}/"
          dn: uni/tn-ACILab/ap-test-ap
          body:
            fvAp:
              attributes:
                rn: ap-test-ap
                name: test-ap
                descr: test application profile
```

See the `test-playbook.yml` for a full example of this. Use `ansible-playbook -i hosts test-playbook.yml` to execute it. 

### Abstracted roles
In order to simplify usage, abstracted roles for any commonly used ACI construct can be built on top of the aci_model module. Currently roles exist for the following:
- application_profile
- epg
- contract
- filter

An example of using these roles can be found in `sample-three-tier-web-app/meta/main.yml`. Use `ansible-playbook -i hosts test-role-playbook.yml` to execute it. 
