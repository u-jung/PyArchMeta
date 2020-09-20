import os
import sys
import json
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import unittest
from pyarchmeta import meta, helper, factory, aggregation, xml_


class MetaDataObjectTest(unittest.TestCase):
    """Test the MetaDataObject and sub class"""
    
    def setUp(self):
        print("--> MetaDataObjectTest.setUp")
        self.ino1 = meta.InformationObject(1, "L'art de l'archivage.", "fr")
        self.ino2 = meta.InformationObject()
        self.apo1 = meta.AccessPoint(123456789, "Musterhausen" )
        self.apo2 = meta.AccessPoint()
        self.teo1 = meta.Term(2,"Serie","")
        self.teo2 = meta.Term()
        self.aco1 = meta.Actor(3,"Mustermann, Max")
        self.aco2 = meta.Actor()
        self.reo1 = meta.Repository("Bundesarchiv")
        self.reo2 = meta.Repository()
        self.loo1 = meta.LevelOfDescription(4,"Archivtektonik")
        self.loo2 = meta.LevelOfDescription()
        
        
    def test_set_attr(self):
        print("--> MetaDataObjectTest.test_set_attr")
        self.ino1.set_attr("legacyId",123)
        self.ino2.set_attr_dict({
            "parent_id":456,
            "title":"Hallo Welt", 
            "subjectAccessPoints":["Softwaretest","First Code"]
            })
        self.ino2.set_attr("title","Hello world!","en")
        self.apo1.set_attr("name","Livre","fr")
        self.ino2.set_attr("genre_access_points",self.apo1)
        self.ino2.set_attr("subject_access_points","Anwendungsfall","de")

    def test_output(self):
        print("--> MetaDataObjectTest.test_output")
        print('self.ino1.to_json(lang= "fr", with_none= False, simplify = False)')
        print(self.ino1.to_json(lang= "fr", with_none= False, simplify = False))
        print('self.ino1.to_json(lang= "fr", with_none= False, simplify = True)')
        print(self.ino1.to_json(lang= "fr", with_none= False, simplify = True))
        print('self.ino1.to_json(lang= "de", with_none= False, simplify = True)')
        print(self.ino1.to_json(lang= "de", with_none= False, simplify = True))
        print('self.apo1')
        print(self.apo1)       
        

class AggregationTest(unittest.TestCase):
    
    def setUp(self):
        print("--> Aggregation.setUp")
        self.ioa = aggregation.InformationObjectAggregation()
        
    
    def test_append(self):
        print("--> Aggregation.test_append")
        for i,e in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"): 
            self.ioa.append(meta.InformationObject(i,e))
        print("len: ",len(self.ioa))
        
    def test_remove(self):
        print("--> Aggregation.test_remove")
        print("len: ",len(self.ioa))
        self.ioa.remove_by_key("Q","title")
        print("len (after remove): ",len(self.ioa))
        
    def test_output(self):
        print("--> Aggregation.test_output")
        self.test_append()
        self.test_remove()
        print('self.ioa.to_json()')
        print(self.ioa.to_json(simplify=True, with_none=False))
        print("Statistics:", self.ioa.statistics())
        #print('self.ioa[0]')
        #print(self.ioa[0])
        #print('self.ioa')
        #print(self.ioa)
    
    def test_read_from_xml(self):
        print("--> Aggregation.test_read_from_xml")
        xml_obj = xml_.XML_()
        result= xml_obj.load("ead3_multi_level_optimum.xml")
        #result= xml_obj.load("NL-TbRAT-115_916_maximal.xml")
        r=xml_obj.read()
        print("->>",result)
        
        print(json.dumps(r.to_json(simplify=False, with_none=False),indent=2))


class XMLTest(unittest.TestCase):
    
    def setUp(self):
        pass
    
    
    def test_validate(self):
        print("--> XMLTest.test_validate")
        xml_obj = xml_.XML_("ead3_multi_level_optimum.xml")
        print ("Result", xml_obj.validate_xsd())
    



if __name__ == "__main__": 
    unittest.main()
