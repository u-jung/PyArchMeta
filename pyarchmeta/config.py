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
            "id_":"int",
            "legacy_id":"int",
            "parent_id":"int",
            "qubit_parent_slug":"str",
            "identifier":"str",
            "accession_number":"str",
            "title":"dict",
            "level_of_description":"str",
            "extent_and_medium":"dict",
            "repository":"dict",
            "archival_history":"dict",
            "acquisition":"dict",
            "scope_and_content":"dict",
            "appraisal":"dict",
            "accruals":"dict",
            "arrangement":"dict",
            "access_conditions":"dict",
            "reproduction_conditions":"dict",
            "language":"dict",
            "script":"dict",
            "language_note":"dict",
            "physical_characteristics":"dict",
            "finding_aids":"dict",
            "location_of_originals":"dict",
            "location_of_copies":"dict",
            "related_units_of_description":"dict",
            "publication_note":"dict",
            "digital_object_URI":"str",
            "general_note":"dict",
            "subject_access_points":"list.access_point",
            "place_access_points":"list.access_point",
            "name_access_points":"list.access_point",
            "genre_access_points":"list.access_point",
            "description_identifier":"str",
            "institution_identifier":"str",
            "rules":"dict",
            "description_status":"dict",
            "level_of_detail":"dict",
            "revision_history":"dict",
            "language_of_description":"dict",
            "script_of_description":"dict",
            "sources":"dict",
            "archivist_note":"dict",
            "publication_status":"dict",
            "physical_object_name":"dict",
            "physical_object_location":"dict",
            "physical_object_type":"dict",
            "alternative_identifiers":"list",
            "alternative_identifier_labels":"list",
            "event_dates":"str",
            "event_types":"str",
            "event_start_dates":"str",
            "event_end_dates":"str",
            "event_descriptions":"str",
            "event_actors":"list",
            "event_actor_histories":"list",
            "event_places":"list",
            "culture":"dict",
            "status":"int",
            "key_map":"str",
            "prediction":"float",
            "validation":"int"
             }

    TERM_TYPES=("acces_point","level_of_description")

    ACCESS_POINT_TYPES = ("subject","genre","place","name")
    
    REPOSITORY_FIELDS = {}
    
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
            "parent_id":"int"
            }

    CORE_FIELDS = {
            "name",
            "title",
            "authorized_form_of_name"
            }
    

    def __init__(self):
        f = open("pyarchmeta/config","r")
        dict_ = {}
        try:
            dict_ = json.load(f)
        except:
            print ("Please make sur you have a valif config file")
        if dict_ == {}:
            self.SECRETS = {}
        else:
            self.SECRETS = dict_
        
