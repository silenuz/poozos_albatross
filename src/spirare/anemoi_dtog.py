#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 6/7/26
@File: anemoi_dtog

@Author: Silenuz Nowan (silenuznowan@yahoo.com)

Contains Data Transfer Objects for Godot
"""
from typing import TypedDict, NotRequired


class PropertyInfo(TypedDict):
    """
    In a Godot GDExtension, PropertyInfo is used to describe a property's type, name, hint, and usage flags so
    the engine can properly display it in the Inspector

        :param variant_type: The Godot Variant::Type of the property (e.g., Variant::INT, Variant::STRING, Variant::VECTOR3)
        :type variant_type: str
        :param property_name: The name of the property as it will be accessed in GDScript and the editor
        :type property_name: str
    """
    variant_type: str
    """The Godot Variant::Type of the property (e.g., Variant::INT, Variant::STRING, Variant::VECTOR3)"""
    property_name: str
    """The name of the property as it will be accessed in GDScript and the editor"""
    hint: NotRequired[str]
    """(Optional): A PropertyHint that tells the editor how to display or constrain the value (e.g., PROPERTY_HINT_RANGE, PROPERTY_HINT_ENUM)."""
    hint_string: NotRequired[str]
    """(Optional): Extra information for the hint. For ranges, it's "min,max,step". For enums, it's a comma-separated list of names."""
    usage_flags: NotRequired[str]
    """(Optional): A PropertyUsageFlags combination determining how the property behaves (e.g., PROPERTY_USAGE_DEFAULT, PROPERTY_USAGE_READ_ONLY)."""
    class_name: NotRequired[str]
    """ (Optional): Used if the type is a Resource or Object and you want to specify the exact class type"""