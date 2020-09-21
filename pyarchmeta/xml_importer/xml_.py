from lxml import etree
import json
import sys
import os
import pkg_resources    
from pyarchmeta import factory, meta, aggregation, helper
from pyarchmeta.config import GlobalConst


class XML_():
    
    
    xmlschema = None
    so = helper.StringOps()
    lo = helper.ListOps()
    oo = helper.OtherOps()
    element_mapping = {}
    date_mapping = {}
    ignore_tags = ("p", "part")
    stop_tags = ('c', 'c01', 'c02', 'c03', 'c04', 'c05', 'c06', 'c07', 'c08', 'c09', 'c10', 'c11', 'c12')

    
    def __init__(self):
        resource_package = __name__
        self.xsd_path = '/'.join(('pyarchmeta','xml', 'ead3.xsd')) 
        self.xml_path = ""
        self.tree = None
        self.namespaces = None
        self.ns = None
        self.element_mapping = self._load_mapping()["element_mapping"]
        self.date_mapping = self._load_mapping()["date_mapping"]
        self.aggregations = {
                            "InformationObjectAggregation":[],
                            "RepositoryAggregation":[],
                            }



    def load(self, filename: str) -> any:
        """Load a XML document into the object"""
        self.xml_path = '/'.join(('tmp', filename)) 
        try:
            self.tree = etree.parse(self.xml_path)
            self.namespaces = dict([node for _,node in etree.iterparse(self.xml_path, events=['start-ns'])])
            self.namespaces["empty"] = self.namespaces.pop("")
            self.namespaces["re"] = "http://exslt.org/regular-expressions"
            return self.tree.getroot()
        except OSError:
            return "Could not load file " + self.xml_path

    
    def validate_xsd(self) -> bool:
        if self.xmlschema is None:
            self.xmlschema = etree.XMLSchema(file= self.xsd_path)
            parser = etree.XMLParser(schema = self.xmlschema)
            try:
                tree = etree.parse(self.xml_path, parser)
                return True
            except etree.XMLSyntaxError:
                return False
            

    def read(self):
        """Wrap the get_items method"""
        return self.get_items()
    
    def get_aggregations(self, key_: str = "InformationObjectAggregation"):
        """Return a list of creted aggregations"""
        if key_ in self.aggregations:
            return self.aggregations[key_]
    
    def _remove_ns(self, tag_: str) -> str:
        """Clean the element tag string and remove the {namespace} part"""
        return tag_.split("}")[-1]
    
    def _load_mapping(self):
        """Load the data from the mapping file"""
        currentdir = os.path.dirname(os.path.realpath(__file__))
        filename = currentdir + "/" +(self.__class__.__name__).lower() + ".conf"
        try:
            f = open(filename, "r")
            str_ = ("").join([line[:-1] for line in f.readlines() if not line.startswith("#")])
            dict_ = json.loads(str_)
            f.close()
            return dict_
        except KeyError:
            print ("Could not load", filename, "file")
            return {}
        
        
                
    def __str__(self):
        return str({
            "xsd_path":self.xsd_path,
            "xml_path":self.xml_path,
            "tree": self.tree,
            "namespaces":self.namespaces,
            "ns":self.ns 
        })

    def _iterdesc(self, element: any = None, only: list=[] , 
                until: list = [], join: str = "|", format_: str = "str",
                 *args, **kwargs) -> any:
        str_ = ""
        for e in element.iterdescendants():
            if isinstance(e, etree._Comment):
                continue
            tag_ = self._get_short_tag(e)
            text_ = self.so.strip_non_printable(e.text)
        
            if tag_  not in only:
                break
            if tag_ in until:
                break
            if tag_ not in self.ignore_tags:
                str_+= "{" + tag_ + "} " 
            if text_ == "":
                str_+= "|"
            else:
                str_+= " " + text_
            str_ = ("|").join([x for x in str_.split("|") if x.strip() != ""])
        return self.so.clean_ends(str_,"|")
