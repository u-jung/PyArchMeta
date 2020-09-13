import json

from pyarchmeta.helper import StringOps
from pyarchmeta.config import GlobalConst
from pyarchmeta import factory


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
    
    def __init__(self, id_: int = None, default: str = ""):
        self.id_= id_
        for key_,value_ in self.FIELDS.items():
            self.__setattr__(key_, None)
        if default != "":
            self.set_attr(self._main_attr(), default)
        #return self
         
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
            
    def is_valid(self) -> bool:
        """[DEFAULT] Check if all attr has value_ which is not None"""
        if len([key_ for key_, value_ in self.__dict__.items() if value_ is None]) == 0:
            return True
        else:
            return False
    
    def to_json(self, lang: str = "", with_none: bool = True, 
            fall_back: bool = True, simplify: bool = False, *args, **kwargs) -> dict:
        
        """Give the object attributes as dictionary.
        
        Parameters:
        lang – prefered language (all languages if lang = '')
        with_none – if True attributes with None values will be given
        fall_back – if True the value will give in the fall back language 
                    if there is no value in prefered language
        simplify – if True sub dicts will be give only the default string
                     in the preferend language. This depass with_none.
        """
        dict_ = {}
        
        for key_,value_ in self.__dict__.items():
            #print (type(value_), key_, value_)
            if value_ is None:
                if with_none:
                    dict_[key_] = value_
            if isinstance(value_, (str, int, float)) :
                dict_[key_] = value_
            if isinstance(value_,list):
                list_ = []
                for e in value_:
                    if simplify and isinstance(e, MetaDataObject):
                        list_.append(e.default(lang))
                    else:
                        list_.append(e.to_json(lang,with_none, fall_back, simplify))
                if simplify:
                    dict_[key_] = "|".join(list_)
                else:
                    dict_[key_] = list_.copy()
            if isinstance(value_, dict):
                if simplify and self._simplify(value_,lang):
                    dict_[key_] = self._simplify(value_,lang)
                else: 
                    ddict_ = {}
                    for dkey_, dvalue_ in value_.items():
                        if isinstance(dvalue_,dict):
                            if simplify:
                                ddict_[dkey_] = self._simplify(dvalue_, lang)
                            else:
                                if lang == "":
                                    if with_none:
                                        ddict_[dkey_] = dvalue_.copy()
                                    else:
                                        ddict_[dkey_] = {k: v for k, v in dvalue_.items() if v is not None}
                                else:
                                    if dvalue_[lang] is None:
                                        ddict_[dkey_] = dvalue_[self.LANGUAGES[0]]
                                    else:
                                        ddict_[dkey_] = dvalue_[lang]
                        else:
                            if with_none:
                                ddict_[dkey_] = dvalue_
                            else:
                                if dvalue_ is not None:
                                    ddict_[dkey_] = dvalue_
                    if lang != "" and lang in value_:
                        if lang in ddict_ and ddict_[lang] is not None:
                            dict_[key_] = {lang: ddict_[lang]}
                        else:
                            dict_[key_] = {self.LANGUAGES[0]: ddict_[self.LANGUAGES[0]]}
                    else:
                        dict_[key_] = ddict_.copy()                        
        return dict_.copy()

            
    def default(self, lang: str= GlobalConst.LANGUAGES[0]):
        """Retrieve the main value of the object in the given language"""
        dict_ = self.__dict__[self._main_attr()]
        if isinstance(dict_, dict):
            return self._simplify(dict_,lang)
        else:
            return dict_[lang]
    
    def read(self):
        """Read object information from database"""
        pass
    
    def data(self):
        """Return the object dict"""
        return self.__dict__
    
    def write(self):
        """Write object information from database"""
        pass

    def is_valid(self):
        """Check if the object is valid"""
        pass

    def to_str(self):
        """Give a formated object representation"""
        json_ = str(self.__dict__)
        return json.dumps(json_, indent=2)
    
    def has_id(self):
        """Check if the there is a not None attr id_"""
        if self.id_ is not None:
            return True
        else:
            return False
    
    def has_value(self,attr: str, value_: any, lang: str = "") -> any:
        """Check if a given attr has a specific value"""
        if lang == "":
            lang = self.LANGUAGES[0]
        result = False
        if isinstance(self.__dict__[attr],MetaDataObject):
            result =  self.__dict__[attr].has_value(self.__dict__[attr]._main_attr(),value_)
            if result:
                return self
        if isinstance(self.__dict__[attr],(int, str, float)):
            if self.__dict__[attr] == value_:
                result = self
        if isinstance(self.__dict__[attr],list):
            for e in self.__dict__[attr]:
                if isinstance(e,MetaDataObject):
                    result =  e.has_value(e._main_attr(),value_)
                    if result:
                        return self
                else:
                    if e == value_:
                        result = self
        if isinstance(self.__dict__[attr],dict):
            for k, v in self.__dict__[attr].items():
                if isinstance(v, dict):
                    if lang in v and v[lang] == value_:
                        return self
                else:
                    if v == value_:
                        return self
        return False
                    
            
    
    
    def generate_from(self, attr: str, json_out: bool) -> any:
        """Generate items from specific attr"""
        if isinstance(self.attr,(list,tuple)):
            for e in self.__dict__[attr]:
                if isinstance(e,MetaDataObject) and json_out:
                    e=e.to_json()
                yield e
        if isinstance(self.attr, dict):
            for key_, value_ in self.attr:
                yield (k,v)
        if isinstance(self.attr,(str,int,float)):
            yield e
        
        
    
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

    def _main_attr(self) -> str:
        """Get the main attribute"""
        fields = set(GlobalConst.__dict__[self.so.to_underscore(type(self).__name__).upper() + "_FIELDS"].keys())
        field = list(fields.intersection(GlobalConst.CORE_FIELDS))
        if len(field)>0:
            return field[0]
        else:
            return ""
    
    def _simplify(self, dict_: dict, lang: str="") -> str:
        """Give the simple default value from a sub dict"""
        if lang == "":
            lang = self.LANGUAGES[0]
        if lang in dict_:
            if dict_[lang] is None:
                return dict_[self.LANGUAGES[0]]
            else:
                return dict_[lang]
        else:
            if self._main_attr in dict:
                return _simplify(dict_[self._main_attr], lang)
            return None
    
    
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
                list_.append(e)
            else:
                type_ = self.FIELDS[attr].split(".")[1]
                if type_ == "list":
                    list_.append(e)
                else:
                    list_.append(self._sub_object_factory(type_,e))
        self.__setattr__(attr,list_.copy()) 
        return True
        
    def _set_attr_object(self, attr: str, value_: any, lang: str) -> bool:
        result = self._set_attr_dict(attr, value_, lang)
        return result
        
    def _sub_object_factory(self, type_: str, main_, str="") -> bool:
        """Create a sub object depending from type"""
        if type_ == "access_point":
            object_ = AccessPoint(None, main_)
        if type_ == "term":
            object_ = Term(None, main_)
        if type_ == "information_object":
            object_ = InformationObject(None, main_)
        if type_ == "actor":
            object_ = Actor(None, main_)
        if type_ == "repository":
            object_ = Repository(None, main_)
        return object_
        
    
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
        print(self.to_json())
        return str(self.to_json())
    
    def __str__(self):
        return self.__class__.__name__ +"("+json.dumps(self.to_json(), indent=2)+")"
        
    def __eval__(self, other: any) -> bool:
        if self.__dict__ == other.__dict__:
            return True
        else:
            return False
            
    def __ne__(self, other: any) -> bool:
        if self.__dict__ == other.__dict__:
            return False
        else:
            return True





class InformationObject(MetaDataObject):
    """Manage the information object"""
  
    FIELDS = GlobalConst.INFORMATION_OBJECT_FIELDS
    
    def __init__(self, id_: int = None, default: str = ""):
        """ initialize the instance """
        super().__init__(id_, default)
        #print (type(self.LANGUAGES), self.LANGUAGES[0], 
        #    GlobalConst.LANGUAGES, GlobalConst.SECRETS["MYSQLOPS"])
        self.id_ = id_
        #return self
        
                
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
    
    def __init__(self, main_: str = "",taxonomy: str = None):
        super().__init__()
        self.taxonomy = taxonomy
        if main_ != "":
            self.set_attr(self._main_attr(), main_)
    pass

class Actor(MetaDataObject):
    """Manage the actor"""
    FIELDS = GlobalConst.ACTOR_FIELDS
    
    def __init__(self, id_: int = None, main_: str = ""):
        super().__init__()

class Repository(MetaDataObject):
    """Manage the repository."""
    
    FIELDS = GlobalConst.REPOSITORY_FIELDS
    
    def __init__(self, id_: int = None, main_: str = ""):
        super().__init__()
    

class AccessPoint(Term):
    """Manage an Access Point"""
    FIELDS = GlobalConst.ACCESS_POINT_FIELDS
    TYPES = GlobalConst.ACCESS_POINT_TYPES
    
    def __init__(self, id_: int = None, main_: str = ""):
        super().__init__()
        if main_ != "":
            self.set_attr(self._main_attr(), main_)
        
       
  

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
        
    def __init__(self, id_: int = None, main_: str = ""):
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


