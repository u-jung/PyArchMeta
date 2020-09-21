import json


class GlobalConst():
    
    
    # Languages, which are used in parallel (!). First element is the fallback language
    LANGUAGES = [
        "de",
        "en",
        "fr"
    ]
    SECRETS = {
        "MYSQLOPS":{
        "host":"localhost",
        "user":"root",
        "pass":"",
        "db":""
        },
        "APIKEYS" : {
        }
    
    }
    
    INFORMATION_OBJECT_FIELDS = {
            "access_conditions":"dict",
            "accession_number":"str",
            "accruals":"dict",
            "acquisition":"dict",
            "alternative_identifier_labels":"list",
            "alternative_identifiers":"list",
            "appraisal":"dict",
            "archival_history":"dict",
            "archivist_note":"dict",
            "arrangement":"dict",
            "biografical_history":"dict",
            "container":"str",
            "culture":"dict",
            "description_identifier":"str",
            "description_status":"dict",
            "digital_object_URI":"str",
            "event_actor_histories":"list",
            "event_actors":"list",
            "event_dates":"str",
            "event_descriptions":"str",
            "event_end_dates":"str",
            "event_places":"list",
            "event_start_dates":"str",
            "event_types":"str",
            "extent_and_medium":"dict",
            "finding_aids":"dict",
            "general_note":"dict",
            "genre_access_points":"list.access_point",
            "identifier":"str",
            "id_":"int",
            "institution_identifier":"str",
            "key_map":"str",
            "language":"dict",
            "language_note":"dict",
            "language_of_description":"dict",
            "legacy_id":"int",
            "level_of_description":"object.level_of_description",
            "level_of_detail":"dict",
            "location_of_copies":"dict",
            "location_of_originals":"dict",
            "name_access_points":"list.access_point",
            "origination":"list.access_point",
            "parent_id":"int",
            "physical_characteristics":"dict",
            "physical_object_location":"dict",
            "physical_object_name":"dict",
            "physical_object_type":"dict",
            "place_access_points":"list.access_point",
            "prediction":"float",
            "publication_note":"dict",
            "publication_status":"dict",
            "qubit_parent_slug":"str",
            "related_units_of_description":"dict",
            "repository":"dict",
            "reproduction_conditions":"dict",
            "revision_history":"dict",
            "rules":"dict",
            "scope_and_content":"dict",
            "script":"dict",
            "script_of_description":"dict",
            "sources":"dict",
            "status":"int",
            "subject_access_points":"list.access_point",
            "title":"dict",
            "validation":"int"
             }

    TERM_TYPES=("acces_point","level_of_description")

    ACCESS_POINT_TYPES = ("subject","genre","place","name")
    
    REPOSITORY_FIELDS = {
        "corpname":"dict",
        "identifier":"str",
        "desc_status_id":"int",
        "desc_detail_id":"int",
        "desc_identifier":"str",
        "upload_limit":"float",
        "source_culture":"str",
        "geocultural_context" :"dict",
        "collecting_policies":"dict",
        "buildings":"dict",
        "holdings":"dict",
        "finding_aids":"dict",
        "opening_times":"dict", 
        "access_conditions":"dict",
        "disabled_access":"dict",
        "research_services":"dict", 
        "reproduction_services":"dict",
        "public_facilities":"dict",
        "desc_institution_identifier":"dict", 
        "desc_rules":"dict",
        "desc_sources":"dict",
        "desc_revision_history":"dict",
    
    }
    
    ACTOR_FIELDS = {
            "id_":"int",
            "entity_type_id":"int",
            "description_identifier":"str",
            "parent_id":"int",
            "authorized_form_of_name ":"dict",
            "dates_of_existence":"str",
            "history":"dict",
            "places":"dict",
            "legal_status":"dict",
            "functions":"dict",
            }
    
    TERM_FIELDS = {
            "id_":"int",
            "name":"str",
            "parent_id":"int"
            }
            
    ACCESS_POINT_FIELDS = {
            "id_":"int",
            "wikidata":"str",
            "ap_type":"str",
            "name":"dict",
            "parent_id":"int",
            "identifier":"str"
            }
    
    LEVEL_OF_DESCRIPTION_FIELDS ={
        "id_":"int",
        "name":"dict",
        "parent_id":"int"
            
    }

    CORE_FIELDS = {
            "name",
            "title",
            "authorized_form_of_name",
            "corpname"
            }
    
    ISO639 = {
     'ger': 'de', 
	 'eng': 'en', 
	 'fre': 'fr', 
	 'spa': 'es', 
	 'prt': 'pt', 
	 'rus': 'ru', 
	 'jpn': 'jp', 
	 'zho': 'zh', 
	 'ita': 'it', 
	 'dan': 'dk', 
	 'swe': 'sw', 
	 'nld': 'nl', 
	 'pol': 'pl', 
	 'ara': 'ar', 
	 'tur': 'tk',
     'dut': 'nl'}
    
    
   

    def __init__(self):
        f = open("pyarchmeta/config.json","r")
        dict_ = {}
        try:
            dict_ = json.load(f)
        except:
            print ("Please make sur you have a valif config file")
        if dict_ == {}:
            self.SECRETS = {}
        else:
            self.SECRETS = dict_
        

