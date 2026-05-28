#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 5/28/26
@File: gen_class_doc

@Author: Phosphor (horuuendillus@gmail.com)
"""
import sys
from pathlib import Path

# Get the absolute path to this script
script_path = Path(__file__).resolve()

# Get the absolute path to the directory containing the python scripts
spirare_script_dir = script_path.parent.parent / 'src' / 'spirare'
sys.path.append(str(spirare_script_dir))

# class document generator needs two arguments, where to look for the doxygen content
# and where to put the generated class XML documentation, for this example
# the documentation is placed in the doc_classes_generated directory
doxygen_xml_output = script_path.parent / 'doxygen_output'
doc_classes_directory = script_path.parent / 'doc_classes_generated'

# 1. Set the arguments first xml, destination
sys.argv = ["aerify_didi.py",str(doxygen_xml_output),str(doc_classes_directory)]

# run the script
import aerify_didi
aerify_didi.parse_class_xml_files()