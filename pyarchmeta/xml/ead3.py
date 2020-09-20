import re

from pyarchmeta import meta, aggregation, xml_, factory
from pyarchmeta.config import GlobalConst
from lxml import etree

class EAD3Access(xml_.XML_):
    """ Manage the Encoded Archival Description Standard , Version 3 XML"""
    
    mapping = {
        "legacy_id":[["unitid","_attr",{"attr":"id"}]],
        "parent_id":[["unitid","_up",{"attr":"id"}]],
        "identifier":[
                ["agency_id","_text",
                    {
                    "other_text":"recordid", 
                    "restriction":"control"
                    }
                ],
                ["unitid","_text",
                    {
                    "attr":['countrycode','repositorycode']
                    }
                ]
                ],
        "title":[
                ["unittitle","_text",{}]],
        "event_dates":[
                    ["unitdate","_text",{}],
                    ["unitdatestructured","_text",{
                        "sub_tags":("daterange", "dateset", "datesingle", "fromdate","todate")
                    }]
                    ],
        "level_of_description":[
                    ["archdesc","_attr",{"attr":"level"}],
                    ["c","_attr",{"attr":"level"}]
        
                ],
        "extent_and_medium":[
                    ["physdesc","_text",{}],
                    ["physdescstructured","_text",{
                        "attr":["physdescstructuredtype", "coverage"],
                        "sub_tags":["quantity","unittype"]
                    }],
                ],
        "origination":[
                    ["origination","_text",{
                        "identifier":["source", "identifier"],
                        "sub_tags":["corpname", "famname", "name", "persname", "part"],
                        "sub_sub_tags":["part"]
                    }]
                ],
        "biografical_history":[
                    ["bioghist","_text",{
                        "sub_tags":("bioghist", "blockquote", "chronlist", "head", "list", "p", "table")
                    }]
                ],
        "archival_history":[
                    ["custodhist","_text",{
                        "sub_tags":("blockquote", "chronlist", "custodhist", "head", "list", "p", "table")
                    }]
                ],
        "acquisition":[
                    ["acqinfo","_text",{
                        "sub_tags":("acqinfo", "blockquote", "chronlist", "head", "list", "p", "table")
                    }]
                ],
        "scope_and_content":[
                    ["scopecontent","_text",{
                        "sub_tags":("scopeconent","blockquote", "chronlist", "head", "list", "p", "table")
                    }]
                ],
        "appraisal":[
                    ["appraisal","_text",{
                        "sub_tags":("appraisal","blockquote", "chronlist", "head", "list", "p", "table")
                    }]
                ],
        "accruals":[
                    ["accruals","_text",{
                        "sub_tags":("accruals","blockquote", "chronlist", "head", "list", "p", "table")
                    }]
                ],
        "arrangement":[
                    ["arrangement","_text",{
                        "sub_tags":("arrangement","blockquote", "chronlist", "head", "list", "p", "table")
                    }]
                ],
        "access_conditions":[
                    ["accessrestrict","_text",{
                        "sub_tags":("accessrestrict","blockquote", "chronlist", "head", "list", "p", "table")
                    }]
                ],
        "reproduction_conditions":[
                    ["userestrict","_text",{
                        "sub_tags":("userestrict","blockquote", "chronlist", "head", "list", "p", "table")
                    }]
                ],
        "language":[
                    ["language", "_attr",{
                        "attr":"langcode",
                        "within":"langmaterial"
                    }]
                ],
        "language_note":[
                    ["language", "_text",{
                        "within":"langmaterial"
                    }]
                ],
        "script":[
                    ["script", "_attr",{
                        "attr":"scriptcode",
                        "within":"langdeclaration"
                    }]
                ],
        "physical_characteristics":[
                    ["phystech","_text",{
                        "sub_tags":("phystech","blockquote", "chronlist", "head", "list", "p", "table")
                    }]
                ],
                
        "finding_aids":[
                    ["otherfindaid","_text",{
                        "sub_tags":("otherfindaid","blockquote", "chronlist", "head", "list", "p", "table","archlist","bibref")
                    }]
                ],
        "location_of_originals":[
                    ["originalsloc","_text",{
                        "sub_tags":("originalsloc","blockquote", "chronlist", "head", "list", "p", "table")
                    }]
                ],
        "location_of_copies":[
                    ["altformavail","_text",{
                        "sub_tags":("altformavail","blockquote", "chronlist", "head", "list", "p", "table")
                    }]
                ],
        "related_units_of_description":[
                    ["relatedmaterial","_text",{
                        "sub_tags":("relatedmaterial","blockquote", "chronlist", "head", "list", "p", "table","archref","bibref")
                        }],
                    ["separatedmaterial","_text",{
                        "sub_tags":("separatedmaterial","blockquote", "chronlist", "head", "list", "p", "table","archref","bibref")
                        }],
                ],
        "publication_note":[
                    ["bibliography","_text",{
                        "sub_tags":("bibliography","blockquote", "chronlist", "head", "list", "p", "table","archref","bibref")
                    }]
                ],
        "general_note":[
                    ["didnote","_text",{
                        "sub_tags":("abbr", "emph", "expan", "foreign", "lb", "ptr", "ref")
                        }],
                    ["odd","_text",{
                        "sub_tags":("odd","blockquote", "chronlist", "head", "list", "p", "table")
                        }],
                ],
        "archivist_note":[
                    ["processinfo","_text",{
                        "sub_tags":("processinfo","blockquote", "chronlist", "head", "list", "p", "table")
                    }]
                ],
        "rules":[
                    ["conventiondeclaration","_text",{
                        "sub_tags":("abbr", "citation", "descriptivenote"),
                        "within":"control"
                    }]
                ],
        "event_descriptions":[
                    ["maintenanceevent","_text",{
                        "sub_tags":("agent", "agenttype", "eventdatetime", "eventdescription", "eventtype"),
                        "within":"maintenancehistory"
                        }],
                    ["eventdatetime","_text",{
                        "within":"maintenancehistory"
                        }],
                ],
        "container":[
                    ["container","_text",{
                        "sub_tags":("abbr", "emp", "expan", "foreign", "lb", "ptr", "ref")
                    }]
                ],
        "digital_object_URI":[["dao","_attr",{"attr":"href"}]],
        "place_access_points":[
                    ["geogname","_text",{
                        "sub_tags":("part", "geographiccoordinates"),
                        "within":"controlaccess",
                        "identifier":("identifier","source")
                        }],
                ],
        "genre_access_points":[
                    ["genreform","_text",{
                        "sub_tags":("part"),
                        "within":"controlaccess",
                        "identifier":("identifier","source")
                        
                        }],
                ], 
        "subject_access_points":[
                    ["subject","_text",{
                        "sub_tags":("part"),
                        "within":"controlaccess",
                        "identifier":("identifier","source")
                        
                        }],
                    ["occupation","_text",{
                        "sub_tags":("part"),
                        "within":"controlaccess",
                        "identifier":("identifier","source")
                        
                        }]
                ], 
        "name_access_points":[
                    ["name","_text",{
                        "sub_tags":("part"),
                        "within":"controlaccess",
                        "identifier":("identifier","source")
                        
                        }],
                    ["corpname","_text",{
                        "sub_tags":("part"),
                        "within":"controlaccess",
                        "identifier":("identifier","source")
                        
                        }],
                    ["persname","_text",{
                        "sub_tags":("part"),
                        "within":"controlaccess",
                        "identifier":("identifier","source")
                        
                        }]
                ],
        "recordid":[
                    ["recordid","_text",{
                        "attr":("instanceurl"),
                        "within":"control"
                    }]
                ],
        "titleproper":[
                    ["titleproper","_text",{
                        "attr":("render"),
                        "sub_tags":( "p", "table"),
                        "within":"titlestmt"
                    }]
                ],
        "subtitle":[
                    ["subtitle","_text",{
                        "attr":("render"),
                        "sub_tags":( "p", "table"),
                        "within":"titlestmt"
                    }]
                ],
        "author":[
                    ["author","_text",{
                        "sub_tags":( "p", "table"),
                        "within":"titlestmt"
                    }]
                ],
        "sponsor":[
                    ["sponsor","_text",{
                        "sub_tags":( "p", "table"),
                        "within":"titlestmt"
                    }]
                ],
        "languagedeclaration":[
                    ["languagedeclaration","_text",{
                        "sub_tags":( "p", "table"),
                        "within":"control"
                    }]
                ],
        "localcontrol":[
                    ["localcontrol","_text",{
                        "sub_tags":( "p", "table"),
                        "within":"control"
                    }]
                ],
        "localtypedeclaration":[
                    ["localtypedeclaration","_text",{
                        "sub_tags":( "p", "table"),
                        "within":"control"
                    }]
                ],
        "maintenanceagency":[
                    ["maintenanceagency","_text",{
                        "sub_tags":( "p", "table"),
                        "within":"control"
                    }]
                ],
        "maintenancehistory":[
                    ["maintenancehistory","_text",{
                        "sub_tags":( "p", "table"),
                        "within":"control"
                    }]
                ],
        "maintenancestatus":[
                    ["maintenancestatus","_text",{
                        "sub_tags":( "p", "table"),
                        "within":"control"
                    }]
                ],
        "otherrecordid":[
                    ["otherrecordid","_text",{
                        "sub_tags":( "p", "table"),
                        "within":"control"
                    }]
                ],
        "publicationstatus":[
                    ["publicationstatus","_text",{
                        "sub_tags":( "p", "table"),
                        "within":"control"
                    }]
                ],
        "representation":[
                    ["representation","_text",{
                        "sub_tags":( "p", "table"),
                        "within":"control"
                    }]
                ],
        "rightsdeclaration":[
                    ["rightsdeclaration","_text",{
                        "sub_tags":( "p", "table"),
                        "within":"control"
                    }]
                ],
        "rightsdeclaration":[
                    ["rightsdeclaration","_text",{
                        "sub_tags":( "p", "table"),
                        "within":"control"
                    }]
                ],
                
    }



    
    
    def __init__(self, xml_path: str, tree: any, namespaces: set ):
        super().__init__()
        self.tree = tree
        self.namespaces = namespaces
        self.xml_path = xml_path
        if "" in namespaces:
            self.namespaces["empty"] = self.namespaces[""]
            self.namespaces.pop("",None)
        self.namespaces["re"] = "http://exslt.org/regular-expressions"
        self.recordid = "?"

        
        
        
    def get_items(self):
        try:
            tmp = self.tree.xpath("//empty:control/empty:languagedeclaration/empty:language", 
                    namespaces = self.namespaces)
            self.lang = self.oo.transform_iso_639(tmp[0].attrib["langcode"], None)[1]
        except IndexError:
            self.lang = GlobalConst.LANGUAGES[0]
        result = self._get_items_control()
        result = self._get_collection( )
        return result
        
        
    def _get_items_control(self):
        """Retrieve general information"""
        tmp = self.tree.xpath("//empty:repository/empty:corpname//text()", 
                namespaces = self.namespaces)
        tmp = self.lo.join_non_empty(tmp," - ")
        rep = meta.Repository(None,tmp, self.lang)
        tmp = self.tree.xpath("//empty:repository/empty:address//text()", 
                namespaces = self.namespaces)
        tmp = self.lo.join_non_empty(tmp," - ")       
        rep.set_attr("buildings",self.lo.join_non_empty(tmp,""), self.lang)
    
    
    def _get_collection(self):
        """Retrieve collection information"""
        tmp = self.tree.xpath('//empty:dsc/*[re:test(local-name(), "c[0-9]*")]/*[re:test(local-name(), "c[0-9]*")]', 
                namespaces = self.namespaces)
        context = etree.iterparse(self.xml_path)
        tree = etree.parse(self.xml_path)
        root = tree.getroot()
        inoa = aggregation.InformationObjectAggregation()
        id_increment = 1
        
        for element in root.iterdescendants():
            if  isinstance(element,etree._Comment):
                continue
            else:
                tag_ = str(element.tag).split("}")[-1]
                element.attrib["tag_"] = tag_
            if element.attrib["tag_"] == "recordid":
                if "instanceurl" in element.attrib:
                    self.recordid = element.attrib["instanceurl"]
                else:
                    self.recordid = element.text
                    
            if re.search("^c[0-9]*$", element.attrib["tag_"]) or element.attrib["tag_"] == "archdesc":
                element.attrib["id_"] = str(id_increment)
                id_increment += 1
                ino = meta.InformationObject()
                result = self._get_id(ino, element)
                result = self._get_parent(ino, element)
                ino = self._retrieve_item(ino, element)
                inoa.append(ino,False)
        return(inoa)
                
    def _get_id(self, ino: any, element: any) -> bool:
        """ Write the legacy_id to the element."""
        if "id" in element.attrib:
            ino.set_attr("legacy_id", element.attrib["id"])
        else:
            ino.set_attr("legacy_id", element.attrib["id_"])
        return True
    
    
    def _get_parent(self, ino: any, element: any) -> bool:
        """ Write the parent_id to the element. """
        if element.attrib["tag_"] != "archdesc":
            el = element.getparent()
            if el.tag.endswith("dsc"):
                el = el.getparent()
            if "id" in el.attrib:
                ino.set_attr("parent_id", el.attrib["id"])
            else:
                ino.set_attr("parent_id", el.attrib["id_"])
            return True
        return False
        
    
    def _retrieve_item(self, ino: any, start_element: any) -> bool:
        """ Fill the InformationObject with data. """
        if "level" in start_element.attrib:
            ino.set_attr("level_of_description", 
                        start_element.attrib["level"],self.lang)
        for el in start_element.iterdescendants():
            if re.search("^c[0-9]*$",self._get_short_tag(el)):
                break
            mapping = self._get_mapping_element(el)
            if mapping:
                ino = self._processor(ino,attr=mapping["attr"], element = el, function_=mapping["func"], params=mapping["param"])
        return ino

    def _get_short_tag(self, element: any) -> str:
        """Return the simple tag (without namespace)"""
        try:
            return element.tag.split("}")[-1]
        except AttributeError:
            return "?"
        

    def _get_mapping_element(self, element: any) -> dict:
        """ Retrieve the function related to the given element"""
        if isinstance(element, etree._Element):
            tag_ = self._get_short_tag(element)
            for key_, value_ in self.mapping.items():
                for i,e in enumerate(value_):
                    if e[0] == tag_:
                        if "within" in e[2]:
                            if e[2]["within"] != self._get_short_tag(element.getparent()):
                                print(tag_," is sub of ", self._get_short_tag(element.getparent()), "instead", e[2]["within"])
                                return None
                        return {"attr": key_,
                                "elem": e[0],
                                "func": e[1],
                                "param": e[2]
                                }
        return None

    
    def _processor(self, ino: any, attr: str, element: any, function_: str, params: dict, *args, **kwargs) -> any:
        """Select a function to retrieve the information for a specific tag"""
        if function_ == "_text":
            return self._text(ino, attr, element, params)
        if function_ == "_attr":
            return self._attr(ino, attr, element, params)
        if function_ == "_up":
            return self._up(ino, attr, element, params)
        return ino
    
    
    def _attr(self, ino: any, attr: str, element: any, params: dict) -> None:
        """Read an attribut from the given element"""
        
        if params["attr"] in element.attrib:
            ino.set_attr(attr,element.attrib[params["attr"]],self.lang)
        return ino
    
    def _up(self, ino: any, attr: str, element: any, params: dict)-> None:
        pass
        
        
    def _text(self, ino: any, attr: str, element: any, params: dict)-> None:
        """Read texts from element and sub elements."""
        #print("---",element.tag)
        element_text = self.so.strip_non_printable(element.text)
        if "sub_tags" in params:
            only = params["sub_tags"]
        else:
            only=[]
        children_ = (self._iterdesc(element=element,
                    only=only, until=self.stop_tags)).strip(" ")
                    
        if attr == "event_dates":
            dates_ = self._make_dates(children_, element)
            ino.set_attr("event_dates", dates_["event_dates"])
            ino.set_attr("event_start_dates", dates_["event_start_dates"])
            ino.set_attr("event_end_dates", dates_["event_end_dates"])
                    
        if len(ino.FIELDS[attr].split(".")) == 2:
            obj_ = factory.Factory(ino.FIELDS[attr].split(".")[1],
                    children_, self.lang).get_product()
            if "identifier" in params:
                identifier = "|".join([element.attrib[x] for x in params["identifier"] if x in element.attrib])
                
                obj_.set_attr("identifier", identifier)
                ino.set_attr(attr, obj_)
        else:
            format_ = "str"
            children_text = self._iterdesc(element=element,
                        only=only, until=self.stop_tags, format_=format_)
            composition = "|".join([element_text, children_text]).strip("|")
            ino.set_attr(attr, composition, self.lang)
        return ino
    

    
    def _getpath(self, elem: any, anonym_path: str) -> str:
        """Rebuild the xpath of an element"""
        xpath=elem.tag
        list_ = anonym_path.split("/*")
        print(list_)
        xpath = xpath + list_[-1]
        for i in range(len(list_)-1,0,-1):
            elem = elem.getparent()
            if elem is not None:
                xpath=elem.tag + list_[i-1]+"/" + xpath
        return xpath

    def _make_dates(self, dates_str_: str, element:any) -> dict:
        """Create a dict with different date information"""

        dates = dates_str_.replace("{dateset}","")
        dates = dates.replace("{daterange}","")
        dates = dates.replace("{fromdate}","")
        dates = dates.replace("|","")
        dates = dates.replace("{todate}","-")
        dates = dates.replace("{datesingle}",", ")
        dates = dates.replace(" ","")
        dates = dates.strip(" ")
        dates = dates.strip(",")
        dates = dates.replace(",",", ")
        return {"event_dates": dates,
                "event_start_dates":"",
                "event_end_dates":""
                }
