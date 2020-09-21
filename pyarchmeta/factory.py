from pyarchmeta import meta
#from pyarchmeta.xml import ead3
from pyarchmeta.config import GlobalConst

class Factory():
    """Create an instance of an MetaDataObject."""
    
    def __init__(self, type_: str, default: str="", lang: str = GlobalConst.LANGUAGES[0], *args, **kwargs):
        """Create a sub object depending from type"""
        object_ = None
        if type_ in ("access_point", "AccesPoint"):
            self.object_ = meta.AccessPoint(None, default, lang)
        if type_ in ("term", "Term"):
            self.object_ = meta.Term(None, default, lang)
        if type_ in ("information_object", "InformationObject"):
            self.object_ = meta.InformationObject(None, default, lang)
        if type_ in ("actor", "Actor"):
            self.object_ = meta.Actor(None, default, lang)
        if type_ in ("repository", "Repository"):
            self.object_ = meta.Repository(None, default, lang)
            
        #if type_ in ("ead3"):
            #self.object_ = ead3.EAD3Access(xml_path= kwargs["xml_path"], tree= kwargs["tree"], namespaces= kwargs["namespaces"])
            #self.object_ = ead3.EAD3Access()
        
    def get_product(self):
        """Get the produced object"""
        return self.object_
        
