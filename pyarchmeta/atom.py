from pyarch.archival_description import InformationObject, AccessPoint, LevelOfDescription
from pyarch.config import GlobalConst
from pyarch.database import MySQLDatabase

__all__ = [
    "AtomAccessPoint",
    "AtomLevelOfDescription"
    ]

class AtomObject():
    """Manage object representation from AtoM database"""
    
    def __init__(self):
        self.id_ = None
        
    def set_id(self, id_: int) -> bool:
        self.id_ = id_
        return True
    
    def get_id(self) -> int:
        return self.id_
        

class AtomI18NObject(AtomObject):
    """Manage object i18n representation in AtoM database"""
    g= GlobalConst()
    LANGUAGES = g.LANGUAGES

    def __init__(self):
        super().__init__()
        for e in self.LANGUAGES:
            self.__setattr__(e,None)
        
    def __setattr__(self, name, value):
        self.__dict__[name] = value
        
    def set_attr_i18n(self,attr: str = g.LANGUAGES[0], value_: str = "") -> bool:
        if attr.lower in g.LANGUAGES and isinstance(value_, str):
            self.__setattr__(attr.lower(), value_)
            return True
        else:
            return False
    
    def _fill_from_db(self, id_: int) -> None:
        pass

class AtomInformationObject(InformationObject, AtomObject):
    """Manage an AtoM InformationObject representation"""
    
    def __init__(self):
        super().__init__()
        
    def to_json(self) -> dict:
        return self.__dict__
        
        
class AtomAccessPoint(AccessPoint, AtomI18NObject):
    """Manage an AtoM AccessPoint representation"""
    TABLES = ["term", "term_i18n"]
    
    def __init__(self):
        super().__init__()
        
    def to_json(self) -> dict:
        return self.__dict__
    
    def get_record(self, id_: int) -> dict:
        db = MySQLDatabase()
        dict_ = db.get_row_by_id(self.TABLES[0],id_)
        return dict_
        
        
class AtomLevelOfDescription(LevelOfDescription, AtomI18NObject):
    """Manage an AtoM LevelOfDescription respresentation"""
    TABLES = ["term", "term_i18n"]

    def __init__(self):
        super().__init__()
        
    def to_json(self) -> dict:
        return self.__dict__
        
    
        

"""class AtomAccessPoint(AccessPoint, AtomI18NObject):
    
    def __init__(self):
        self.id_ = None
        super().__init__()
        
    def set_attr(self, attr: str, value_: any) -> bool:
        print(self.__dict__)
        super().set_attr(attr,value_)
        if attr == "id_":
            if str(value_).isnumeric():
                self.__setattr__(attr,int(value_))
            else:
                return False
    
    def set_atom_object_id(self, int_: int) -> bool:
        if str(int_).isnumeric():
            self.id_=int(int_)
            return True
        else:
            return False
            
    def get_id(self) -> int:
        return self.id_
        
    def to_json(self, lang: str ="") -> dict:
        if lang=="":
            lang = self.LANGUAGES[0]
        return super().to_json(lang)
    

class AtomLevelOfDescription(LevelOfDescription):
    
    def __init__(self):
        self.id_ = None
        super().__init__()"""
