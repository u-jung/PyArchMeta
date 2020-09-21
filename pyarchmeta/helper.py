import re
import string

from pyarchmeta.config import GlobalConst

class StringOps():
    """Operate withs strings"""
    def to_capitalized(self,str_: str) -> str:
        """Transform a symbol name from lower_case_with_underscores to CapitalizedWords."""
        return re.sub(r'[_]+(?P<first>[a-z])', 
                      lambda m: m.group('first').upper(), 
                      str_)

    def to_underscore(self,str_ : str) -> str:
        """Transform a symbol name from CapitalizedWords to lower_case_with_underscores."""
        return re.sub(r'(?P<first>[A-Z])', 
                      lambda m: "_" + m.group('first').lower(), 
                      str_).strip("_")
                      
                      
    def strip_non_printable(self,str_: str) -> str:
        return re.sub(r'\n|\t','',str_)
    
    def clean_leading(self, str_: str, chars: str) -> str:
        """ strip first characters  of a string """
        chars += " "
        i = 0
        for i,c in enumerate(str_):
            if c not in chars:
                break
        str_ = str_[i:]
        return str_
        
    def clean_trailing(self, str_: str, chars: str) -> str:
        """ strip last characters of a string """
        str_ = str_[::-1]
        str_ = self.clean_leading(str_,chars)
        str_ = str_[::-1]
        return str_
    
        
    def clean_ends(self, str_: str, chars: str) -> str:
        """Wrap the clean_leading and the clean_trailing methods"""
        str_ = self.clean_leading(str_,chars)
        return self.clean_trailing(str_,chars)

class ListOps():
    """Operate with lists"""
    
    def join_non_empty(self,list_, delimiter: str = "|"):
        return (delimiter).join([x for x in list_ if (StringOps().strip_non_printable(x)).strip("") != ""])


class OtherOps():
    """Operate"""
    
    def transform_iso_639(self,three_letter: str = None, two_letter: str = None, default: bool = False) -> tuple:
        """transform ISO 639-3 to iso 639-2"""
        if three_letter is not None:
            if three_letter in GlobalConst.ISO639:
                two_letter = GlobalConst.ISO639[three_letter]
            else:
                if default:
                    two_letter = GlobalConst.LANGUAGES[0]
                else:
                    two_letter = "??"
        else:
            if two_letter in GlobalConst.ISO639.values():
                three_letter = [v for k,v in GlobalConst.ISO639.items() if v == two_letter][0]
            else:
                three_letter = "???"
        return (three_letter, two_letter)

    def alter_lang_code(self, lang: str) -> str:
        """Alter the given lang code into another (2 or 3 letter code)"""
        if len(lang) == 3:
            if lang in GlobalConst.ISO639:
                return GlobalConst.ISO639[lang]
        if len(lang) == 2:
            if lang in GlobalConst.ISO639.values():
                for key_, value_ in GlobalConst.ISO639:
                    if value_ == lang:
                        return key_
        return lang                
        
