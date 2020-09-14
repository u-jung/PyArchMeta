import json

from pyarchmeta import meta, factory
from pyarchmeta.config import GlobalConst

class Aggregation(list):
    """Manage aggregation of MetaDataObjects"""
    
    def __init__(self):
        self.list_ = []
        self.i=0
        
    
    def add(self, meta_data_object: any, check_uniq: bool = True) -> bool:
        """Add a MetaDataObject to the aggregation"""
        if check_uniq:
            if len(self.get_items(meta_data_object)) == 0:
                self.list_.append(meta_data_object)
                return True
            else:
                if self.duplicate_test(meta_data_object):
                    return False
                else:
                    self.list_.append(meta_data_object)
                    return True
        else:
            self.list_.append(meta_data_object)
            return True
    
    def add_dict(self, dict_: dict, check_uniq: bool = True) -> bool:
        """Add a json representation to the aggregation"""
        cls = self.__class__.__name__.split("Aggre")[0]
        fac = factory.Factory(cls)
        product = fac.get_product()
        product.set_attr_dict(dict_)
        return self.add(product)
        
    def remove(self, meta_data_object: any) -> bool:
        """Remove MetaDataObject from Aggregation. Return number of items found."""
        try:
            self.list_.remove(meta_data_object)
            return True
        except ValueError:
            return False
    
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
                    if x.has_value(key_,value_,lang)]
        
    def to_json(self, lang: str = "", with_none: bool = True, 
            fall_back: bool = True, simplify: bool = False, *args, **kwargs):
        return [x.to_json(lang = lang, with_none= with_none, fall_back= fall_back, simplify= simplify) for x in self.list_]
          
    def statistics(self):
        """count used keys in object list"""
        dict_ = {}
        for e in self.list_:
            for k,v in e.data().items():
                if v is not None:
                    if k in dict_ :
                        dict_[k] += 1
                    else:
                        dict_[k] = 1
        return {"len": len(self.list_), "attribute frequencies" : dict_}

    def append(self, meta_data_object: any, check_uniq: bool = True) -> bool:
        """Add an element to the aggregation.
        Wrap the add method
        """
        return self.add(meta_data_object, check_uniq)
    
    def get_items(self, meta_data_object: any, attr: str = "id_") -> list:
        """Check if there is an item in aggregation with same key_attr. 
        Return the first MetaDataObject found if True, else None:
        """
        return [x for x in self.list_ if attr in x.data() and x.data()[attr]]
    
    def duplicate_test(self, meta_data_object: any = None) -> bool:
        """ Check if an MetaDataObject already exists in Aggregation.
        
        Return True if this is the case.
        If no object is given the method perform an integrity test of the given index.
        Return True if there a duplicate primary keys.
        This method use the self.key_attribute value  of "id_" if not given.
        This will not work with key_attribute which is using int or string.
        """
        if meta_data_object is None:
            if len(self) > 0:
                meta_data_object = self.list_[0]
            else:
                return False
        key_attribute_value = meta_data_object.data()[meta_data_object.key_attribute]
        if key_attribute_value is not None:
            if len(self.select_by_key(key_attribute_value, meta_data_object.key_attribute)) > 0:
                return True
            else:
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
        json_ = [x.to_json(simplify= True) for x in self.list_]
        return self.__class__.__name__ +"("+json.dumps(json_, indent=2)+")"
    
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
