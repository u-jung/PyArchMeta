import re

class StringOps():
    def to_capitalized(self,str_: str) -> str:
        """Transform a symbol name from lower_case_with_underscores to CapitalizedWords."""
        return re.sub(r'[_]+(?P<first>[a-z])', 
                      lambda m: m.group('first').upper(), 
                      str_) 

    def to_underscore(self,str_ : str) -> str:
        """Transform a symbol name from CapitalizedWords to lower_case_with_underscores."""
        return re.sub(r'(?P<first>[A-Z])', 
                      lambda m: "_" + m.group('first').lower(), 
                      str_)
