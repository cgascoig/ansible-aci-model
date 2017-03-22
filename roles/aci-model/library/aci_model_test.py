import unittest
import imp

aci_model=imp.load_source("acimodel", "./aci_model")

class TestCompareModel(unittest.TestCase):

    def test_different_base_classes(self):
        d,c,error = aci_model.compare_model({"fvAp": {"attributes":{"rn":"anp-test"}}}, {"fvTenant": {"attributes":{"rn":"anp-test"}}})
        self.assertIsNotNone(error)
    def test_same_base_classes(self):
        d,c,error = aci_model.compare_model({"fvAp": {"attributes":{"rn":"anp-test"}}}, {"fvAp": {"attributes":{"rn":"anp-test"}}})
        self.assertIsNone(error)
        
    #attribute should be changed
    def test_attribute_should_be_changed(self):
        dm = {"fvAp":{
            "attributes": {
                "rn": "anp-test",
                "a": "a"
            }
        }}
        cm = {"fvAp":{
            "attributes": {
                "rn": "anp-test",
                "a": "b"
            }
        }}
        d,c,error = aci_model.compare_model(dm, cm)
        self.assertIsNone(error)
        self.assertDictEqual(c['fvAp']['attributes'],{'a': 'a'})
        self.assertDictEqual(d,{})
    
    #attribute is already correct
    def test_attribute_already_correct(self):
        dm = {"fvAp":{
            "attributes": {
                "rn": "anp-test",
                "a": "a"
            }
        }}
        cm = {"fvAp":{
            "attributes": {
                # "rn": "anp-test",
                "a": "a"
            }
        }}
        d,c,error = aci_model.compare_model(dm, cm)
        self.assertIsNone(error)
        self.assertDictEqual(c,{})
        self.assertDictEqual(d,{})
    
    #attribute should be ignored
    def test_attribute_should_be_ignored(self):
        dm = {"fvAp":{
            "attributes": {
                "rn": "anp-test",
            }
        }}
        cm = {"fvAp":{
            "attributes": {
                "rn": "anp-test",
                "a": "a"
            }
        }}
        d,c,error = aci_model.compare_model(dm, cm)
        self.assertIsNone(error)
        self.assertDictEqual(c,{})
        self.assertDictEqual(d,{})
        
    #attribute should be added
    def test_attribute_should_be_added(self):
        dm = {"fvAp":{
            "attributes": {
                "rn": "anp-test",
                "b":"b"
            }
        }}
        cm = {"fvAp":{
            "attributes": {
                "rn": "anp-test",
                "a": "a"
            }
        }}
        d,c,error = aci_model.compare_model(dm, cm)
        self.assertIsNone(error)
        self.assertDictEqual(c['fvAp']['attributes'], {'b': 'b'})
        self.assertDictEqual(d,{})
        
        
    ##################################################################
    # Child related tests
    ##################################################################
    
    def test_child_should_be_added(self):
        epgweb = {
                    "fvAEPg": {
                        "attributes":{
                            "rn": "web"
                        }
                    }
                }
        dm = {"fvAp":{
            "attributes": {
                "rn": "anp-test",
            },
            "children": [
                epgweb
            ]
        }}
        cm = {"fvAp":{
            "attributes": {
                "rn": "anp-test",
            }
        }}
        d,c,error = aci_model.compare_model(dm, cm)
        self.assertIsNone(error)
        self.assertListEqual(c['fvAp']['children'], [epgweb])
        self.assertDictEqual(d,{})
        
    def test_child_should_be_changed(self):
        epgweb = {
                    "fvAEPg": {
                        "attributes":{
                            "rn": "web",
                            "name": "web"
                        }
                    }
                }
        dm = {"fvAp":{
            "attributes": {
                "rn": "anp-test",
            },
            "children": [
                epgweb
            ]
        }}
        cm = {"fvAp":{
            "attributes": {
                "rn": "anp-test"
            },
            "children": [
                {
                    "fvAEPg": {
                        "attributes":{
                            "rn": "web",
                        }
                    }
                }
            ]
        }}
        d,c,error = aci_model.compare_model(dm, cm)
        
        del epgweb['fvAEPg']['attributes']['rn']
        
        self.assertIsNone(error)
        self.assertListEqual(c['fvAp']['children'], [epgweb])
        self.assertDictEqual(d,{})
        
    def test_child_should_be_removed(self):
        epgweb = {
                    "fvAEPg": {
                        "attributes":{
                            "rn": "web",
                            "name": "web"
                        }
                    }
                }
        dm = {"fvAp":{
            "attributes": {
                "rn": "anp-test",
            },
            "children": []
        }}
        cm = {"fvAp":{
            "attributes": {
                "rn": "anp-test"
            },
            "children": [
                epgweb
            ]
        }}
        d,c,error = aci_model.compare_model(dm, cm)
        
        del epgweb['fvAEPg']['attributes']['rn']
        
        self.assertIsNone(error)
        self.assertDictEqual(c,{})
        self.assertListEqual(d['fvAp']['children'], [epgweb])

if __name__ == '__main__':
    unittest.main()