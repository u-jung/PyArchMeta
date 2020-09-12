
from ..archiv.lib.ArchivalDescription import InformationObject, AtomAccessPoint

ino=InformationObject()

ino.set_attr("legacyId",123)
a="parent_id"

print("--")
print(ino.set_attr_dict({"parent_id":456,"title":"hello world", "subjectAccessPoints":["Kamerun","Jaunde"]}))

print(ino.set_attr("subject_access_points","Wald"))

ap=AtomAccessPoint()
ap.set_attr("atom_object_id",9876)
ap.set_attr("de","Straße")
print(ino.set_attr("subject_access_points",ap))

print (ino.to_json(), ap)
#print (ino._walk(ino))

print("?", isinstance(ino,InformationObject))




