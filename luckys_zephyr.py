#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 5/27/26
@File: luckys_zephyr

@Author: Phosphor (horuuendillus@gmail.com)
"""
from collections import namedtuple
from pathlib import Path
from xml.etree import ElementTree as et

ClassInfo = namedtuple("ClassInfo", ["class_name", "reference"])

def get_class_name(data_node: et.Element) -> ClassInfo:
    class_name = data_node.attrib['id']
    name = class_name.replace("class", "")
    reference_node  = data_node.find('includes')
    reference = reference_node.attrib['refid']
    return ClassInfo(name, reference)

def create_profile_for_class(file: Path)->tuple[et.Element, ClassInfo]:
    tree = et.parse(file)
    root = tree.getroot()
    data_node = root[0]
    class_info = get_class_name(data_node)
    return data_node,class_info