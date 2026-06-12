#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 6/11/26
@File: poozo_sample

@Author: Silenuz Nowan (silenuznowan@yahoo.com)
"""
import sys
from pathlib import Path
from src.spirare.poozos_notus import PoozoNotus

# Get the absolute path to this script
script_path = Path(__file__).resolve()

# Get the absolute path to the directory containing the python scripts
spirare_script_dir = script_path.parent.parent / 'src' / 'spirare'
sys.path.append(str(spirare_script_dir))

traffic_light_path = script_path.parent.parent / 'example' / 'src' / 'traffic_light.cpp'
summator_path = script_path.parent.parent / 'example' / 'src' / 'summator.cpp'
traffic_light_parser = PoozoNotus(traffic_light_path)
summator_parser = PoozoNotus(summator_path)

## get bound integer constants
## recent refactors mean this method needs the name of the class to amp get_class_static() to
bound_integer_constants = summator_parser.get_bound_constants("Summator")
for bound_constant in bound_integer_constants:
    print(bound_constant)

# get bound methods that were bound using dmethod macro
# traffic light has no methods so we use summator here
bound_methods_set = summator_parser.get_bound_methods()
for bound_method in bound_methods_set:
    print(bound_method)

# get bound properties, summator has no properties
# use traffic light source instead
bound_properties = traffic_light_parser.get_bound_properties()
for bound_property in bound_properties:
    print(bound_property)

# get bound signals, both files have signals, but traffic light has usage flags
bound_signals = traffic_light_parser.get_bound_signals()
for bound_signal in bound_signals:
    print(bound_signal)
