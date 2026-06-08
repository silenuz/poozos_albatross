#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 6/7/26
@File: anemoi_dtog

@Author: Silenuz Nowan (silenuznowan@yahoo.com)

Contains Data Transfer Objects for Godot
"""
from __future__ import annotations
from dataclasses import dataclass, field
import shlex
from typing import List


def split_arg_string(arg_string: str) -> str:
    lexer = shlex.shlex(arg_string, posix=True)
    lexer.whitespace = ','  # Tell it to split on commas
    lexer.whitespace_split = True  # Only split on whitespace (commas)
    args_list = [arg.strip() for arg in lexer]
    return args_list

@dataclass()
class IntegerConstantModel:
    """
    Data Model to hold information about constant integer bindings in the source code.
    """
    p_class: str
    """p_class_name value"""
    p_enum: str
    """p_enum_value value"""
    p_name: str
    """p_constant_name value"""
    p_value: str
    """p_constant_value value"""
    p_is_bitfield: bool = False
    """is bitfield value"""

    @classmethod
    def from_arg_string(cls, arg_string: str):
        args = split_arg_string(arg_string)
        # expected CSV structure
        field_names = [
            "p_class",
            "p_enum",
            "p_name",
            "p_value",
            "p_is_bitfield"
        ]
        kwargs = dict(zip(field_names, args))
        return cls(**kwargs)

@dataclass()
class MemberDefinitionModel:
    """
    Used to model data from the Doxygen XML Memberdef elements
    """
    member_type: str
    """data type if a field the data type of the field, if a function the return type of the function"""
    definition: str
    """member definition data value followed by qualified name, ex: int Summator::get_total """
    member_name: str
    """simple name portion of the method or member name"""
    qualified_name: str
    """qualified name of the method or member"""
    brief: str | None = None
    """brief description of the method or member"""
    description: str | None = None
    """detailed description of the method or member"""
    initializer: str | None = None
    """for constants and enumerators this indicates the initial value """
    arg_string: str | None = None
    """If applicable contains the argument string for the member"""


@dataclass()
class MethodInfoModel:
    """
    MethodInfo Data Model

    Used to model a MethodInfo declaration in CPP code.

    CPP USAGE:
    1. Name only (No arguments, no return value / void)
          MethodInfo(const StringName &p_name);
   2. Name followed by a variable number of PropertyInfo arguments(Used for signals and void methods)
         MethodInfo(const StringName &p_name, const PropertyInfo &p_p1);
         MethodInfo(const StringName &p_name, const PropertyInfo &p_p1, const PropertyInfo &p_p2);
   3. Explicit Return Value FIRST, then Name, then arguments (Used for methods that return a value)
         MethodInfo(const PropertyInfo &p_return_val, const StringName &p_name);
    """
    name: str
    argument_info: List[PropertyInfoModel] = field(default_factory=list)
    return_info: PropertyInfoModel | None = None

    def __post_init__(self):
        # Fallback to an empty list if None was passed so we can just loop it without worry
        if self.argument_info is None:
            self.argument_info = []


@dataclass()
class PropertyInfoModel:
    """
    PropertyInfo Data Model

    In a Godot GDExtension, PropertyInfo is used to describe a property's type, name, hint, and usage flags so
    the engine can properly display it in the Inspector

        :param variant_type: The Godot Variant::Type of the property (e.g., Variant::INT, Variant::STRING, Variant::VECTOR3)
        :type variant_type: str
        :param name: The name of the property as it will be accessed in GDScript and the editor
        :type name: str
    """
    variant_type: str
    """The Godot Variant::Type of the property (e.g., Variant::INT, Variant::STRING, Variant::VECTOR3)"""
    name: str
    """The name of the property as it will be accessed in GDScript and the editor"""
    hint: str | None = None
    """(Optional): A PropertyHint that tells the editor how to display or constrain the value (e.g., PROPERTY_HINT_RANGE, PROPERTY_HINT_ENUM)."""
    hint_string: str | None = None
    """(Optional): Extra information for the hint. For ranges, it's "min,max,step". For enums, it's a comma-separated list of names."""
    usage_flags: str | None = None
    """(Optional): A PropertyUsageFlags combination determining how the property behaves (e.g., PROPERTY_USAGE_DEFAULT, PROPERTY_USAGE_READ_ONLY)."""
    class_name: str | None = None
    """ (Optional): Used if the type is a Resource or Object and you want to specify the exact class type"""
    index: int = 0

    def get_hint_type(self) -> tuple[str, str]:
        # todo: rename soon as possible
        if self.hint is None and self.usage_flags is None:
            return None

        if self.hint is not None:
            if self.hint_string is not None and self.hint == "PROPERTY_HINT_RESOURCE_TYPE":
                return "type", self.hint_string
            elif self.hint == "PROPERTY_HINT_ENUM":
                if self.class_name:
                    return "enum", self.class_name
                else:
                    return "enum", None

        if self.usage_flags is not None:
            if "PROPERTY_USAGE_CLASS_IS_ENUM" in self.usage_flags:
                return 'enum', self.class_name

        return None

    @property
    def index_string(self) -> str:
        return str(self.index)

    @property
    def variant_type_name(self) -> str:
        return self.variant_type.split("::")[1].lower()

    @classmethod
    def from_arg_string(cls, arg_string: str, index: int = 0):
        """
        Creates a PropertyInfo from a string containing the PropertyInfo arguments
        :param index: optional index to track the position of the property info, in a list or property info args
        :param arg_string: csv string containing the PropertyInfo arguments
        :return: PropertyInfo
        """
        args = split_arg_string(arg_string)
        if len(args) < 2:
            print("invalid number of arguments, a property Info requires at least the variant type and property name")
            return None
        # expected CSV structure
        field_names = [
            "variant_type",
            "name",
            "hint",
            "hint_string",
            "usage_flags",
            "class_name"]
        kwargs = dict(zip(field_names, args))
        kwargs["index"] = index
        return cls(**kwargs)

    @dataclass()
    class PropertyModel:
        """
        Data Model for Bound properties parsed from source code
        """
        field: str
        """Member name"""
        getter: str
        """Name of the method to get the member value"""
        setter: str
        """Name of the method to set the member value"""
        info: PropertyInfoModel
        """PropertyInfo model containing the information from the source code declaration"""

