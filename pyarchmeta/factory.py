from pyarchmeta import meta

class Factory():
    """Create an instance of an MetaDataObject."""
    
    def __init__(self, type_: str, default: str=""):
        """Create a sub object depending from type"""
        object_ = None
        if type_ in ("access_point", "AccesPoint"):
            self.object_ = meta.AccessPoint(None, default)
        if type_ in ("term", "Term"):
            self.object_ = meta.Term(None, default)
        if type_ in ("information_object", "InformationObject"):
            self.object_ = meta.InformationObject(None, default)
        if type_ in ("actor", "Actor"):
            self.object_ = meta.Actor(None, default)
        if type_ in ("repository", "Repository"):
            self.object_ = meta.Repository(None, default)
        
    def get_product(self):
        """Get the produced object"""
        return self.object_
        
