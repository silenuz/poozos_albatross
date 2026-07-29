#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 7/9/26
@File: eurus_sample

@Author: Silenuz Nowan (silenuznowan@yahoo.com)
"""
import sys
from pathlib import Path
import xml.etree.ElementTree as Et

from spirare.eurus import Eurus

# Get the absolute path to this script
script_path = Path(__file__).resolve()

main_directory = script_path.parent.parent

# Get the absolute path to the directory containing the python scripts
spirare_script_dir = main_directory / 'src' / 'spirare'
sys.path.append(str(spirare_script_dir))

extension_example_directory = main_directory / 'example'
xml_folder = extension_example_directory / 'doxygen_output'
output_folder = script_path.parent / 'eurus_samples'

if not output_folder.exists():
    output_folder.mkdir()

# set extension directory so that eurus can find the necessary source code to parse for bindings.
eurus = Eurus(extension_example_directory)
files = list(Path(xml_folder).rglob('class*.xml'))

for file in files:
    class_doc = eurus.load_doxy_class_xml(file)
    xml_element = class_doc.to_xml_doc()
    Et.indent(xml_element, "    ")
    Et.register_namespace('xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    xsi_namespace = "{http://www.w3.org/2001/XMLSchema-instance}"
    xml_element.set(xsi_namespace + "noNamespaceSchemaLocation",
                    "https://raw.githubusercontent.com/godotengine/godot/master/doc/class.xsd")
    tree = Et.ElementTree(xml_element)
    file_name = file.stem + '.xml'
    file_path = output_folder / file_name
    tree.write(str(file_path), encoding="utf-8", short_empty_elements=False, xml_declaration=True)
