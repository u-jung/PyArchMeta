import json

from pyarchmeta.helper import StringOps
from pyarchmeta.config import GlobalConst


__all__ = [
    "MetaDataObject",
    "InformationObject",
    "Actor",
    "Repository",
    "Term",
    "AccessPoint",
    "LevelOfDescription"
    ]


class MetaDataObject():
    """This is the super class for meta data"""

    LANGUAGES = GlobalConst.LANGUAGES
    so = StringOps()
    
    def __init__(self, id_: int = None):
        self.id_= id_
        for k,v in self.FIELDS.items():
            self.__setattr__(k, None)
         
    def set_attr(self, attr: str, value_: any, lang: str = GlobalConst.LANGUAGES[0]) -> bool:
        """Set an attribute."""
        attr = self.so.to_underscore(attr)
        if attr in self.FIELDS:
            if self.FIELDS[attr] == "dict":
                result = self._set_attr_dict(attr, value_, lang)
            if self.FIELDS[attr] == "str_i18n":
                result = self._set_attr_str_i18n(attr,str(value_), lang)
            if self.FIELDS[attr] == "str":
                result = self._set_attr_str(attr,str(value_))
            if self.FIELDS[attr] in ("int","float"):
                result = self._set_attr_numeric(attr,value_)
            if self.FIELDS[attr].startswith("list"):
                result = self._set_attr_list(attr, value_, lang, True)    
            if self.FIELDS[attr].startswith("object"):
                result = self._set_attr_object(attr, value_, lang)
        else:
            return False
        return True        
    
    def set_attr_dict(self, dict_: dict) -> bool:
        """Set attributes according to key, values from a dict."""
        if isinstance(dict_, dict):
            result = True
            for key_,value_ in dict_.items():
                print(key_,value_)
                if not self.set_attr(key_,value_):
                    result = False
        else:
            result = False
        return result
    
    def get_attr(self, attr: str) -> any:
        """Get an attribute"""
        if attr.lower() in self.__dict__:
            return self.__getitem__(attr.lower())
        else:
            return None

    def to_json(self, lang: str = "", with_none: bool = True, fall_back: bool = True) -> dict:
        """Give the object attributes as dictionary """
        dict_={}
        if lang == "":  
            dict_ = self.__dict__
        else: 
            for key_, value_ in self.__dict__.items():
                #print(key_, value_)
                if isinstance(value_, dict):
                    dict_[key_] = value_[lang]
                    if dict_[key_] is None and fall_back:
                        dict_[key_] = value_[self.LANGUAGES[0]]
                if isinstance(value_,list):
                    list_items_=[]
                    for e in value_:
                        if isinstance(e,dict):
                            fields = [x for x in e.keys() if x in GlobalConst.CORE_FIELDS]
                            #print("fields", fields, value_.keys())
                            if len(fields)>0:
                                if isinstance(e[fields[0]], dict):
                                    if e[fields[0]][lang] is None and fall_back:
                                        list_items_.append(e[fields[0]][self.LANGUAGES[0]])
                                    else:
                                        list_items_.append(e[fields[0]][lang])
                                    
                                else:
                                    list_items_.append(e[fields[0]])
                        else:
                            list_items_.append(e)
                    dict_[key_] = "|".join(list_items_)
                if isinstance(value_,str):
                    dict_[key_] = value_
                if isinstance(value_,int):
                    dict_[key_] = value_
        if with_none:
            return dict_.copy()
        else:
            return {k:v for k,v in dict_.items() if not v is None}
            
    
    
    def read(self):
        """Read object information from database"""
        pass
    
    def write(self):
        """Write object information from database"""
        pass

    def is_valid(self):
        """Check if the object is valid"""
        pass

    def to_str(self):
        """Give a formated object representation"""
        return self.__str__()
        
    def _walk(self, object_: any ) -> any:
        """BROKEN - Walk throught the object"""
        if isinstance(object_,InformationObject) and not isinstance(object_,str):
            object_ = self.__dict__
            print("dict---")
        if hasattr(object_,"__iter__"):
            if isinstance(object_,list) or isinstance(object_,tuple):
                for e in object_:
                    #print(type(object_), object_)
                    return self._walk(e)
            if isinstance(object_,dict):
                for key_,value_ in object_.items():
                    return self._walk(value_)
            
        else:
            print ("-->",object_)
            return 

    def to_csv(self, path: str = "", lang: str = ""):
        """Give CSV-String"""
        pass

    def _set_attr_str_i18n(self,attr: str, value_: str, lang) -> bool:
        if lang.lower() not in self.LANGUAGES:
            return False
        if attr in self.__dict__:
            dict_ = self.__getitem__(attr)
            dict_[lang] = value_
            self.__setattr__(attr,dict_)
            return True
        else:
            return False
            
    def _set_attr_str(self,attr: str, value_: str) -> bool:
        self.__setattr__(attr, value_)
        return True
            

    def _set_attr_numeric(self, attr: str, value_: any) -> bool:
        if self.FIELDS[attr] == "int":
            if str(value_).isnumeric():
                self.__setattr__(attr,int(value_))
            else:
                return False
        if self.FIELDS[attr] == "float":
            if str(value_).isnumeric():
                self.__setattr__(attr,float(value_))
            else:
                return False

    def _set_attr_dict(self, attr: str, value_: dict, lang) -> bool:
        if isinstance(value_,dict):
            self.__setattr__(attr,value_)
        else:
            if attr in self.__dict__ and self.__dict__[attr] is not None:
                dict_=self.__dict__[attr]
                dict_[lang]=value_
            else:
                dict_ = {x:None for x in self.LANGUAGES}
                dict_[lang] = value_
            self.__setattr__(attr,dict_.copy())
        return True
    
    def _set_attr_list(self, attr: str, value_: list, lang: str, extend: bool) -> bool:
        if not isinstance(value_, list) and not isinstance(value_, tuple):
            value_ = [value_]
        if self.__dict__[attr] is None or not extend :
            list_ = []
        else:
            list_ = self.__dict__[attr]        
        for e in value_:
            if isinstance(e, MetaDataObject):
                list_.append(e.to_json())
            else:
                type_ = self.FIELDS[attr].split(".")[1]
                if type_ == "list":
                    list_.append(e)
                else:
                    json = self._get_object_to_json(type_, e)
                    list_.append(json.copy())
        self.__setattr__(attr,list_.copy()) 
        return True
        
    def _set_attr_object(self, attr: str, value_: any, lang: str) -> bool:
        dict_ = value_.to_json()
        result = self._set_attr_dict(attr, dict_, lang)
        return result
    
    def _get_object_to_json(self, type_: str, value_: any) -> dict:
        fields = set(GlobalConst.__dict__[type_.upper() + "_FIELDS"].keys())
        field = list(fields.intersection(GlobalConst.CORE_FIELDS))
        if len(field)>0:
            field=field[0]
            lang = self.LANGUAGES[0]
            dict_ = {x:None for x in GlobalConst.__dict__[type_.upper() + "_FIELDS"].keys()}
            dict_[field] = {x:None for x in self.LANGUAGES}
            dict_[field][lang] = value_
            return dict_
        else:
            return {} 
   
    def __setattr__(self, name, value):
        self.__dict__[name] = value
    
    def __repr__(self):
        return str(self.__dict__)
    
    def __str__(self):
        return self.__class__.__name__ +"("+json.dumps(self.__dict__, indent=2)+")"





class InformationObject(MetaDataObject):
    """Manage the information object"""
  
    FIELDS = GlobalConst.INFORMATION_OBJECT_FIELDS
    
    def __init__(self, id_: int = None):
        """ initialize the instance """
        super().__init__()
        print (type(self.LANGUAGES), self.LANGUAGES[0], GlobalConst.LANGUAGES, GlobalConst.SECRETS["MYSQLOPS"])
        self.id_ = id_
        pass
        
                
    def _create_access_point_list(self, value_: any, lang) -> list:
        """Create a list of AccessPoints from existing list"""
        if isinstance(value_,list) or isinstance(value_,tuple):
            pass
        else:
            value_ = [value_]
        list_=[]
        for e in value_:
            if isinstance(e,AccessPoint):
                list_.append(e.to_json())
            if isinstance(e,dict):
                list_.append(e.to_json())
            if isinstance(e,str):
                ap = AccessPoint()
                result = ap.set_attr(lang,e)
                list_.append(ap.to_json())
        return list_.copy()
                
                
                
class Term(MetaDataObject):
    """Manage the term object"""
    
    FIELDS = GlobalConst.TERM_FIELDS
    
    def __init__(self, taxonomy: str = ""):
        self.taxonomy = taxonomy
    pass

class Actor(MetaDataObject):
    """Manage the actor"""
    FIELDS = GlobalConst.ACTOR_FIELDS
    
    def __init__(self, id_: int = None):
        super().__init__()

class Repository(MetaDataObject):
    """Manage the repository."""
    
    FIELDS = GlobalConst.REPOSITORY_FIELDS
    
    def __init__(self, id_: int = None):
        super().__init__()
    

class AccessPoint(Term):
    """Manage an Access Point"""
    FIELDS = GlobalConst.ACCESS_POINT_FIELDS
    TYPES = GlobalConst.ACCESS_POINT_TYPES
    def __init__(self, id_: int = None):
        super().__init__()
        
       
  

    def xset_attr(self, attr: str, value_: any) -> bool:
        """Set an attribute."""
        attr = attr.lower()
        if attr in self.__dict__:
            if attr == "type":
                if value_.lower() in self.TYPES:
                    value_ = value_.lower()
                    self.__setattr__(attr, value_)
                else:
                    return False
            if attr.lower() in self.LANGUAGES + ["wikidata"]:
                self.__setattr__(attr.lower(), value_)
            else:
                pass
            
            return True
        else:
            return False

    def xto_json(self, lang: str = GlobalConst.LANGUAGES[0]) -> dict:
        """Export the AccessPoint as dict"""
        if lang == "":
            lang = self.LANGUAGES[0]
        dict_ = {x:None for x in self.LANGUAGES}
        dict_["wikidata"] = None
        dict_["type"] = None
        for e in self.__dict__:
            dict_[e]=self.__dict__[e]
        return dict_


class LevelOfDescription(Term):
    """manage one level of description"""
    
    g= GlobalConst()
    LANGUAGES = g.LANGUAGES
        
    def __init__(self, id_: int = None):
        for e in self.LANGUAGES:
            self.__setattr__(e,None)
        
    def __setattr__(self, name, value):
        self.__dict__[name] = value
    
    def __repr__(self):
        return str(self.__dict__)
    
    def __str__(self):
        return self.__class__.__name__ +"("+json.dumps(self.__dict__, indent=2)+")"  
        
    def set_attr(self, attr: str, value_: any) -> bool:
        """Set an attribute."""
        attr = attr.lower()
        if attr in self.__dict__:
            if attr.lower() in self.LANGUAGES + ["wikidata"]:
                self.__setattr__(attr.lower(), value_)
            else:
                return False
            return True
        else:
            return False


class Aggregation(list):
    """Manage aggregation of MetaDataObjects"""
    
    def __init__(self):
        self.list_ = []
        self.i=0
        
    
    def add(self, MetaDataObject: any, check_uniq: bool = True) -> bool:
        """Add a MetaDataObject to the aggregation"""
        dict_ = MetaDataObject.to_json()
        return self.add_dict(dict_,check_uniq)
    
    def add_dict(self, dict_: dict, check_uniq: bool = True) -> bool:
        """Add a json representation to the aggregation"""
        if dict_["id_"] is None:
            return False
        if check_uniq:
            if dict_["id_"] in [x["id_"] for x in self.list_]:
                return False
            else:
                self.list_.append(dict_.copy())
                return True
        else:
            self.list_.append(dict_.copy())
            return True

    def remove(self, MetaDataObject: any) -> list:
        dict_ = MetaDataObject.to_json()
        return self.remove_dict(dict_)
    
    def remove_dict(self, dict_: dict) -> list:
        list_ = [x for x in self.list_ if x == dict_]
        for e in list_:
            self.list_.remove(e)
        return e
        
    def remove_by_key(self, value_: any, key_: str = "id_", 
                    lang: str = GlobalConst.LANGUAGES[0] ) -> list:
        list_ = self.select_by_key(value_,key_, lang)
        for e in list_:
            self.list_.remove(e)
        return list_
    
    def select_by_key(self, value_: any, key_: str = "id_", 
                    lang: str = GlobalConst.LANGUAGES[0] ) -> list:
        """Select a sub list of items which match a key value condition"""
        return  [x for x in self.list_ 
                    if x[key_]== value_ or self._is_in_lang(x[key_],value_,lang)]
        
    def to_json(self):
        return self.list_
          
    def key_stat(self):
        """Enumerate used keys in object list"""
        dict_ = {}
        for e in self.list_:
            for k,v in e.items():
                if k in dict_:
                    dict_[k] += 1
                else:
                    dict_[k] = 1
        return dict_

    def append(self, value_: dict) -> bool:
        """Add an element to the aggregation"""
        if isinstance(value_, dict) and "id_" in value_:
            self.list_.append(value_)
            return True
        return False
        
    def _is_in_lang(self, dict_: dict, search_value: str, lang: str) -> bool:
        """Check if the language key of a sub dict match with a certain value"""
        if isinstance(dict_, dict):
            if lang in dict_:
                if dict_[lang].strip() == search_value.strip():
                    return True
        elif isinstance(dict_, list):
            return _is_in_lang_list(dict_, search_value, lang)
        return False
                    
    def _is_in_lang_list(self, list_: list, search_value: str, lang: str) -> bool:
        """Check if the list contains a dict which has a language key with the given value"""
        for e in list_:
            if self._is_in_lang(e, search_value, lang):
                return True
                
    def __iter__(self):
        self.i = 0
        for i,e in enumerate(self.list_):
            yield e
    
    def __next__(self):
        if self.i < len(self.list_):
            e = self.list_[self.i]
            self.i += 1
            return e
        else:
            raise StopIteration
    
    def __len__(self):
        return len(self.list_)
        

    def __contains__(self, id_):
        list_ = self.select_by_key(id_)
        if len(list_) > 0:
            return True
        else:
            return False
    
    def __delitem__(self, key_: int) -> bool:
        if self._in_index(key_):
            return self.list_.remove(key_)
    
    def __getitem__(self, key_: int) -> dict:
        if self._in_index(key_):
            return self.list_[key_]
        return None
    
    def __setitem__(self, key_: int, value_: dict) -> bool:
        if self._in_index(key_):
            if isinstance(value_, dict) and "id_" in value_:
                self.list_[key_] = value_.copy()
                return True
        return False
    
    def _in_index(self, key_: int) -> bool:
        if isinstance(key_, int):
            if key_ >-1 and key_ < len(self.list_):
                return True
        return False
            
    def __str__(self):
        return self.__class__.__name__ +"("+json.dumps(self.list_, indent=2)+")"
    
class InformationObjectAggregation(Aggregation):
    """Manage a list of InformationObject"""
    
    def __init__(self):
        super().__init__()
    
    def is_parent(self,  other):
        """Check if an item is the parent of another"""
        return self["parent_id"] == other["legacy_id"]
        
    def __lt__(self, other):
        return self["legacy_id"].__lt__(other)
        
    def __le__(self, other):
        return self["legacy_id"].__le__(other)
        
    def __eq__(self, other):
        return self["legacy_id"].__eq__(other)
        
    def __ne__(self, other):
        return self["legacy_id"].__ne__(other)
        
    def __gt__(self, other):
        return self["legacy_id"].__gt__(other)
        
    def __ge__(self, other):
        return self["legacy_id"].__ge__(other)
        
    
    

class TermAggregation(Aggregation):
    """Manage a list of Term"""
    
    def __init__(self):
        super().__init__()

class ActorAggregation(Aggregation):
    """Manage a list of Actor"""
    
    def __init__(self):
        super().__init__()

class RepositoryAggregation(Aggregation):
    """Manage a list of InformationObject"""
    
    def __init__(self):
        super().__init__()

class AccessPointAggregation(Aggregation):
    """Manage a list of InformationObject"""
    
    def __init__(self):
        super().__init__()
