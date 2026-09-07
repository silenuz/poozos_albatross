#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 8/27/26
@File: lz_sample

@Author: Silenuz Nowan (silenuznowan@yahoo.com)
"""
import sys
from pathlib import Path
from xml.etree import ElementTree as Et
from xml.etree.ElementTree import indent

from spirare.luckys_zephyr import LuckyZephyr

# Get the absolute path to this script
script_path = Path(__file__).resolve()

# Get the absolute path to the directory containing the python scripts
spirare_script_dir = script_path.parent.parent / 'src' / 'spirare'
sys.path.append(str(spirare_script_dir))

# use generated doxygen for the Summator class in the example directory
summator_doxy_class_xml =  script_path.parent.parent / 'example' / 'doxygen_output' / 'xml' / 'classSummator.xml'
traffic_doxy_class_xml =  script_path.parent.parent / 'example' / 'doxygen_output' / 'xml' / 'classTrafficLight.xml'
lz = LuckyZephyr(summator_doxy_class_xml)

############################################
###          Using Models                ###
############################################

# get and print class brief
brief_description = lz.get_class_brief()
print(f'Brief Description:\n {brief_description}')

# get and print class description:
detailed_description = lz.get_class_detail()
print(f'Detailed Description:\n {detailed_description}')

# fields and methods return member definitions
# look up constant value 'MINIMUM_REQUIRED_AMOUNT':
# field can be looked up by name:
member_definition = lz.find_by_name('MINMUM_REQUIRED_AMOUNT')
print(f'\nConstant Details: "{member_definition.name}"')
print(f'Definition Kind: {member_definition.attributes.kind}')
print(f'Description: {member_definition.description}')
print(f'Type: {member_definition.type}')
print(f'Initial Value: {member_definition.initializer_value}')

# fields can also be looked up by qualified name:
member_definition = lz.find_by_qualified('Summator::DOING_OKAY_AMOUNT')
print(f'\nConstant Details: "{member_definition.name}"')
print(f'Definition Kind: {member_definition.attributes.kind}')
print(f'Description: {member_definition.description}')
print(f'Type: {member_definition.type}')
print(f'Initial Value: {member_definition.initializer_value}')

# lookup method by name and print some attributes
member_definition = lz.find_by_name('get_total')
print(f'\nMethod Details: "{member_definition.name}"')
print(f'Definition Kind: {member_definition.attributes.kind}')
print(f'Brief: {member_definition.briefdescription}')
print(f'Description: {member_definition.description}')
# print return type and description
print(f'Return Type: {member_definition.type}')
# doxygen xml
print(f'return description: {member_definition.returns.description}')
# plain text
print(f'return description plain text: {member_definition.returns.text_description}')
# get the file that contains the definition
print(f'File: {member_definition.location.file}')
# get the file contains the implementation
print(f'Implementation: {member_definition.location.bodyfile}')

# use qualified name to look up method and print some attributes:
member_definition = lz.find_by_qualified('Summator::add')
print(f'\nMethod Details: "{member_definition.name}"')
print(f'Kind: {member_definition.attributes.kind}')
print(f'Protection: {member_definition.attributes.prot}')
print(f'ID: {member_definition.attributes.id}')
# plain text
print(f'Brief (Plain): {member_definition.text_brief_description}')
print(f'Description (Plain): {member_definition.text_description}')

# handling arg string and parameters
print(f'args: {member_definition.argsstring}')
for parameter in member_definition.parameters:
    print(f'\tParameter: {parameter.declname}')
    print(f'\tType: {parameter.type}')
    print(f'\tDescription: {parameter.description}')

# enumerators and enumerator values
# no enums in summator so load traffic light class XML
lz = LuckyZephyr(traffic_doxy_class_xml)

# to get a specific enumerator value use the find_enumerator_value method
enum_value = lz.find_enumerator_value('TRAFFIC_LIGHT_GO')
print(f'\nEnum Value description: {enum_value.description}')
print(f'Enum Value Initializer Value: {enum_value.initializer_value}')

# the enum value model also includes the name of the enumerator it belongs to
# enumerators return standard member definitions and can be looked up using the same methods
enum_definition = lz.find_by_name(enum_value.enum)
print(f'\nEnum Details:')
print(f'Name:{enum_definition.name}')
print(f'Definition Kind: {enum_definition.attributes.kind}')
print(f'Description: {enum_definition.description}\nValues:')
for enum_value in enum_definition.enum_values:
    print(f'\tValue Name: {enum_value.name}')
    print(f'\tIntial Value: {enum_value.initializer_value}')
    print(f'\tDescription: {enum_value.description}\n')

# working with xrefitems
# to get xrefitems pass the name of the title to the get_xref_items method
# traffic light signals have no notes or warnings, so switch back to summator
lz = LuckyZephyr(summator_doxy_class_xml)
signals = lz.get_xref_items('Signal')
for signal in signals:
    print(signal.xrefdescription)
    ## in the case of signals the custom alias may have notes and or warnings
    ## use the xrefitem to get the headlines
    headlines = lz.get_headlines_for_xrefitem(signal)
    if len(headlines) > 0:
        print('Headlines:')
    for headline in headlines:
        print(f'\tType: {headline.kind}')
        print(f'\tHeadline: {headline.content}')
    print('\n')

############################################
###          XML Nodes                   ###
############################################

## Look up member definition based on child tag value
xml_element:Et.Element = lz.node_from_child_tag('name','MINMUM_REQUIRED_AMOUNT')
Et.indent(xml_element,"    ")
print(Et.tostring(xml_element,encoding="unicode"))

## look up memberdef element based on a unique attribute like id
## in this case lookup the reset method:
xml_element:Et.Element = lz.node_from_attr('id','classSummator_1a6e8d85e71fc296888b14ca72fa5fe4de')
Et.indent(xml_element,"    ")
print(Et.tostring(xml_element,encoding="unicode"))
# if the returned element is a memberdef element it can be modeled when necessary:
member_definition = lz.model_member_definition(xml_element)
print(f'\nMember Name: "{member_definition.name}"\n')

## elements can also be searched by common attributes
## for example to get all functions from the Doxygen XML
methods_list = lz.search_by_attribute('kind','function')
for method in methods_list:
    definition = lz.model_member_definition(method)
    print(f'\tMethod Name: {definition.name}')

