#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 5/28/26
@File: build_profile

@Author: Phosphor (horuuendillus@gmail.com)
"""
import sys
from pathlib import Path

# Get the absolute path to this script
script_path = Path(__file__).resolve()

# Get the absolute path to the directory containing the python scripts
spirare_script_dir = script_path.parent.parent / 'src' / 'spirare'
sys.path.append(str(spirare_script_dir))

# profile generator needs two arguments, where to look for the doxygen content
# and where to put the build_profile_gen.json file, for this example
# the build profile will be generated in teh example directory.
doxygen_xml_output = script_path.parent / 'doxygen_output'

# 1. Set the arguments first xml, destination
sys.argv = ["waft_gogo.py",str(doxygen_xml_output),str(script_path.parent)]

# run the script
import waft_gogo
waft_gogo.parse_class_xml_files()