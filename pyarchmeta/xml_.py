from lxml import etree
import pkg_resources
from pyarchmeta import factory, meta, aggregation, helper
from pyarchmeta.config import GlobalConst
#from pyarchmeta.xml import ead3



class XMLImporter():
    """Class factory to manage the call of xml converter for import"""
    
    def __init__(self):
        self.domains = GlobalConst.MODULES
    
    def __new__(self, domain: str):
        if domain in self.domains:
            path_ = self.domains[domain]
            
            return ead3.EAD3Access()


class XML_():
    
    
    xmlschema = None
    so = helper.StringOps()
    lo = helper.ListOps()
    oo = helper.OtherOps()
    
    ignore_tags = ("p", "part")
    stop_tags = ('c', 'c01', 'c02', 'c03', 'c04', 'c05', 'c06', 'c07', 'c08', 'c09', 'c10', 'c11', 'c12')

    
    def __init__(self):
        resource_package = __name__
        self.xsd_path = '/'.join(('pyarchmeta','xml', 'ead3.xsd')) 
        self.xml_path = ""
        self.tree = None
        self.namespaces = None
        self.ns = None
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
                
    def Xread(self):
        """Determine the XML namesspace and read the elements"""
        if self.namespaces[''] == "http://ead3.archivists.org/schema/":
            #obj_ = factory.Factory("ead3", xml_path = self. xml_path, tree=self.tree, namespaces= self.namespaces).get_product()
            obj_ = factory.Factory("ead3").get_product()
        return obj_.get_items()
    
    def read(self):
        return self.get_items()
    
    def get_aggregations(self, key_: str = "InformationObjectAggregation"):
        """Return a list of creted aggregations"""
        if key_ in self.aggregations:
            return self.aggregations[key_]
    
    def _remove_ns(self, tag_: str) -> str:
        """Clean the element tag string and remove the {namespace} part"""
        return tag_.split("}")[-1]
                
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
        return self.so.clean_leading(str_,"|")
