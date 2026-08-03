#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 6/30/26
@File: model_sample.py

@Author: Silenuz Nowan (silenuznowan@yahoo.com)
"""
import sys
from pathlib import Path

from spirare.argestes.class_doc import ClassDocModel, ExtensionDocModel
import xml.etree.ElementTree as Et

# Get the absolute path to this script
script_path = Path(__file__).resolve()

# Get the absolute path to the directory containing the python scripts
spirare_script_dir = script_path.parent.parent / 'src' / 'spirare'
sys.path.append(str(spirare_script_dir))

input_folder =  script_path.parent / 'model_samples'
output_folder = script_path.parent / 'model_samples' / 'output'

if not output_folder.exists():
    output_folder.mkdir()

## Vector3i.xml has operators and constructors
## ScrollContainer.xml has theme items
## PackedDataContainer.xml, ConfigFile.xml have returns_error
## can't find annotations anywhere ?
files = input_folder.glob('*.xml')

#######################################
#        XML TO JSON
#######################################

# create model from xml for all xml files in the model_samples directory,
# and then dump the model to json
for file in files:
    ### note the xml file can also be directly loaded using ClassDocModel.from_file(path)
    tree = Et.parse(str(file))
    root = tree.getroot()
    class_doc = ClassDocModel.from_xml(root)
    file_name = file.stem + '.json'
    file_path = output_folder / file_name
    ### XML and JSON files can be created directly from the model
    class_doc.save(file_path)


files = output_folder.glob('*.json')

#######################################
#        JSON TO XML
#######################################

## create model from json for all the json files created above
## dump the model back to xml
for file in files:
    ### instead of loading json first and then creating the model
    ### in this instance the model will be created directly from the file
    ### the same can be done with xml files.
    class_doc = ClassDocModel.from_file(file)
    ### instead of dumping model directly to a file do it the long way:
    xml_element = class_doc.to_xml_doc()
    tree = Et.ElementTree(xml_element)
    file_name = file.stem + '.xml'
    file_path = output_folder / file_name
    tree.write(str(file_path),encoding="utf-8",short_empty_elements=False,xml_declaration=True)

#######################################
#        MERGE MODELS
#######################################

merge_file_incomplete = script_path.parent.parent / 'example' / 'doc_classes_generated' / 'TrafficLight.xml'
merge_file_new_information = input_folder / 'TrafficLight.xml'

### to merge models simply use the models merge method
### load the aerify generated class with the incomplete information from the example directory
class_doc_incomplete = ClassDocModel.from_file(merge_file_incomplete)
### load the version with the extra information used in above samples
class_doc_new_information = ClassDocModel.from_file(merge_file_new_information)
### merge the new complete information with the original, which creates a new model
new_model = class_doc_incomplete.merge(class_doc_new_information)
file_name = 'TrafficLightMergedContent.xml'
file_path = output_folder / file_name
### save xml directly to file
new_model.save(file_path)


#######################################
#        LOAD DIRECTORY OF DOCS
#######################################
# in case anyone is wondering, running the following on the class docs directory
# of the Godot engine (812 classes in my test) takes approximately 7 seconds on my computer (high middle end) and eats about 60MB of mem.
# While memory usage is fairly moderate it shows the significant bottle-necking impact of getting the type hint
# to determine how to create each model.  Once I have a RC I will have to do some heavy profiling to see where I can
# tidy things up
extension_docs = ExtensionDocModel.from_directory(input_folder)

# loop through models and print description as rst text (Note to_rst is not even alpha yet,
# just using it here to test general concept, and have something
# to do in the loop):
for class_doc in extension_docs.class_docs:
    print(f'{class_doc.name}:')
    print(class_doc.brief_description.text_as_rst())