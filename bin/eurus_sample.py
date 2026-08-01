#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 7/9/26
@File: eurus_sample

@Author: Silenuz Nowan (silenuznowan@yahoo.com)

Basically does the same as the aerify script only using the doc model instead of XML to XML.  It finds
all doxygen class xml files in the specified xml_folder, creates a model based on the doxygen xml content and
then saves the model as a gdextension class doc xml file.
"""
import sys
from pathlib import Path

from spirare.argestes import BriefDescription
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
# use the same source code and generated doxygen xml as aerify does, (The example directory)
eurus = Eurus(extension_example_directory)
## get list of doxygen class xml files
files = list(Path(xml_folder).rglob('class*.xml'))

## for each doxygen class XML file, create a model and from the model create a class doc XML file.
for file in files:
    # create model using doxygen XML
    class_doc = eurus.load_doxy_class_xml(file)
    output_file_name = file.stem + '.xml'
    output_file = output_folder / output_file_name
    # create gd extension class doc XML from the model
    # if the file exists it will merge by default pass merge = false to overwrite existing class doc
    # class_doc.to_file(file_path=output_file,merge=False)
    class_doc.to_file(file_path=output_file)

