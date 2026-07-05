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

from spirare.argestes.class_doc import ClassDocModel
import xml.etree.ElementTree as Et

# Get the absolute path to this script
script_path = Path(__file__).resolve()

# Get the absolute path to the directory containing the python scripts
spirare_script_dir = script_path.parent.parent / 'src' / 'spirare'
sys.path.append(str(spirare_script_dir))

input_folder =  script_path.parent / 'samples'
output_folder = script_path.parent / 'samples' / 'output'

if not output_folder.exists():
    output_folder.mkdir()

## Vector3i.xml has operators and constructors
## ScrollContainer.xml has theme items
## PackedDataContainer.xml, ConfigFile.xml have returns_error
## can't find annotations anywhere ?
files = input_folder.glob('*.xml')

# create model from xml for all xml files in the samples directory,
# and then dump the model to json
for file in files:
    ### note the xml file can also be directly loaded using ClassDocModel.from_file(path)
    tree = Et.parse(str(file))
    root = tree.getroot()
    class_doc_three = ClassDocModel.from_xml(root)
    file_name = file.stem + '.json'
    file_path = output_folder / file_name
    with open(file_path, "w", encoding="utf-8") as json_file:
       json_file.write(class_doc_three.to_json())

files = output_folder.glob('*.json')

for file in files:
    ### instead of loading json first and then creating the model
    ### in this instance the model will be created directly from the file
    ### the same can be done with xml files.
    class_doc = ClassDocModel.from_file(file)
    xml_element = class_doc.to_xml_doc()
    Et.indent(xml_element,"    ")
    tree = Et.ElementTree(xml_element)
    file_name = file.stem + '.xml'
    file_path = output_folder / file_name
    tree.write(str(file_path),encoding="utf-8",short_empty_elements=False)
