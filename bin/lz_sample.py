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
from spirare.luckys_zephyr import LuckyZephyr

# Get the absolute path to this script
script_path = Path(__file__).resolve()

# Get the absolute path to the directory containing the python scripts
spirare_script_dir = script_path.parent.parent / 'src' / 'spirare'
sys.path.append(str(spirare_script_dir))

# use generated doxygen for the Summator class in the example directory
summator_doxy_class_xml =  script_path.parent.parent / 'example' / 'doxygen_output' / 'xml' / 'classSummator.xml'
lz = LuckyZephyr(summator_doxy_class_xml)

# get and print class brief
brief_description = lz.get_class_brief()
print(f'Brief Description:\n {brief_description}')

# get and print class description:
detailed_description = lz.get_class_detail()
print(f'Detailed Description:\n {detailed_description}')

# fields and methods return member definitions
# look up constant value 'MINIMUM_REQUIRED_AMOUNT':
# field can be looked up by name:
member_definition = lz.get_definition_by_name('MINMUM_REQUIRED_AMOUNT')
print(f'\nConstant Details:')
print(f'Description: {member_definition.detaileddescription}')
print(f'Type: {member_definition.type}')
print(f'Initial Value: {member_definition.initializer_value}')

# fields can also be looked up by qualified name:
member_definition = lz.get_definition_by_qualified('Summator::DOING_OKAY_AMOUNT')
print(f'\nConstant Details:')
print(f'Description: {member_definition.detaileddescription}')
print(f'Type: {member_definition.type}')
print(f'Initial Value: {member_definition.initializer_value}')

# lookup method by name and print some attributes
member_definition = lz.get_definition_by_name('get_total')
print(f'\nget_total Method Details:')
print(f'Brief: {member_definition.briefdescription}')
print(f'Description: {member_definition.detaileddescription}')
print(f'Return Type: {member_definition.type}')
print(f'File: {member_definition.location.file}')
print(f'Implementation: {member_definition.location.bodyfile}')

# use qualified name to look up method, but print descriptions in plain text
member_definition = lz.get_definition_by_qualified('Summator::add')
print(f'\nadd Method Details:')
print(f'Brief: {member_definition.text_brief_description}')
print(f'Description: {member_definition.text_detailed_description}')
print(f'Return Type: {member_definition.type}')
print(f'File: {member_definition.location.file}')
print(f'Implementation: {member_definition.location.bodyfile}')