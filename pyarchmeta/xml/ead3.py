import re

from pyarchmeta import meta, aggregation, xml_
from pyarchmeta.config import GlobalConst
from lxml import etree

class EAD3Access(xml_.XML_):
    """ Manage the Encoded Archival Description Standard , Version 3 XML"""
    
    mapping = {
        "identifier":(
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
                ),
        "title":[
                ["unittitle","_text",{}]],
        "event_dates":(
                    ["unitdate","_text",{}],
                    ["unitdatestructured","_text",{
                        "sub_tags":("daterange", "dateset", "datesingle", "fromdate","todate")
                    }]
                    ),
        "level_of_description":(
                    ["archdesc","_attr",{"attr":"level"}],
                    ["c","_attr",{"attr":"level"}]
        
                ),
        "extent_and_medium":(
                    ["physdesc","_text",{}],
                    ["physdescstructured","_text",{
                        "attr":["physdescstructuredtype", "coverage"],
                        "sub_tags":["quantity","unittype"]
                    }],
                ),
        "origination":[
                    ["origination","_text",{
                        "attr":["source", "identifier"],
                        "sub_tags":["corpname", "famname", "name", "persname"],
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
        "reproduction_conditions":(
                    ["userestrict","_text",{
                        "sub_tags":("userestrict","blockquote", "chronlist", "head", "list", "p", "table")
                    }]
                ),
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
        "reproduction_conditions":[
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
        "legacy_id":[["unitid","_attr",{"attr":"id"}]],
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
                ]
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
        rep.set_attr("desc_identifier",
                self.tree.xpath("//empty:repository/empty:corpname//@identifier", 
                namespaces = self.namespaces)[0], self.lang )
        #print(rep)
    
    
    def _get_collection(self):
        """Retrieve collection information"""
        tmp = self.tree.xpath('//empty:dsc/*[re:test(local-name(), "c[0-9]*")]/*[re:test(local-name(), "c[0-9]*")]', 
                namespaces = self.namespaces)
        #print("tmp", tmp)
        #print (self.xml_path)
        context = etree.iterparse(self.xml_path)
        inoa = aggregation.InformationObjectAggregation()
        for action, elem in context:
            try:
                if re.search("^.*}c[0-9]*$",elem.tag):
                    ino = meta.InformationObject()
                    #print("\n%s: %s : %s" % (action, elem.tag, elem.getparent().tag))
                    for e in elem.iterdescendants():
                        tag_ = e.tag.split("}")[1]
                        #print (":",tag_, e.tag, e.text)
                        for key_, value_ in self.mapping.items():
                            #print("+++", key_, value_)
                            for i,ee in enumerate(value_):
                                #print(ee,type(ee))
                                if ee[0] == tag_:
                                    #print(e,ee)
                                    self._processor(ino,attr=key_, element = e, function_=ee[1], params=ee[2])
                    if ino:
                        inoa.append(ino,False)
        
            except IndexError:
                print("%s: %s : %s" % (action, elem.tag, ""))
                #print(dir(elem))
        return(inoa)
        

    
    def _processor(self, ino: any, attr: str, element: any, function_: str, params: dict, *args, **kwargs) -> any:
        """Select a function to retrieve the information for a specific tag"""
        if function_ == "_text":
            return self._text(ino, attr, element, params)
        if function_ == "_tag":
            return self._attr(ino, attr,  element, params)
        if function_ == "_up":
            return self.up(ino, attr, element, params)
        return ino
    
    
    def _text(self, ino: any, attr: str, element: any, params: dict):
        #print(element.tag)
        element_text = self.so.strip_non_printable(element.text)
        if "sub_tags" in params:
            only = params["sub_tags"]
            children_text = self._iterdesc(element=element,
                        only=only, until=self.stop_tags)
        else:
            children_text = self._iterdesc(element=element,
                         until=self.stop_tags)
        composition = "|".join([element_text, children_text]).strip("|")
        print("composition", composition, attr)
        ino.set_attr(attr, composition, self.lang)
        return ino
    
    def _attr(self, ino: any, attr: str, element: any, params: dict):
        return ino
        
    def _iterdesc(self, element: any = None, only: list=[] , 
                until: list = [], join: str = "|", *args, **kwargs) -> str:
        str_ = ""
        for e in element.iterdescendants():
            tag_ = self._remove_ns(e.tag)
            text_ = self.so.strip_non_printable(e.text)
            if tag_ not in self.ignore_tags:
                str_+= "{" + tag_ + "} " 
            if text_ == "":
                str_+= "| "
            else:
                str_+= " " + text_
            if tag_  not in only:
                break
            if tag_ in until:
                break
        return str_
    
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

