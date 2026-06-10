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

import re
from dataclasses import dataclass, field
import shlex
from pathlib import Path
from typing import List


def split_arg_string(arg_string: str) -> str:
    lexer = shlex.shlex(arg_string, posix=True)
    lexer.whitespace = ','  # Tell it to split on commas
    lexer.whitespace_split = True  # Only split on whitespace (commas)
    args_list = [arg.strip() for arg in lexer]
    return args_list


class PoozoNotus:
    """
    Class for parsing cpp source code to catalog any bindings.

    "aut, gelidas hibernus aquas cum
    fuderit Auster,
    securum somnos igne iuvante sequi" - Tibullus
    """

    def get_bound_constants(self, class_name: str) -> list[IntegerConstantModel]:
        result = []
        constant_pattern = r'ClassDB::bind_integer_constant\s*\(([\s\S]*?)\)\s*;'
        constant_matches = re.findall(constant_pattern, self.source_code)
        for constant_match in constant_matches:
            # remove comments
            constant_cleaned = re.sub(r"//.*", "", constant_match.replace('get_class_static()', class_name))
            constant_info = IntegerConstantModel.from_arg_string(constant_cleaned)
            result.append(constant_info)
        return result

    def get_bound_enums(self) -> list[str]:
        """

        """
        result = []
        bound_enum_pattern = r"(?<=BIND_ENUM_CONSTANT)\((.*?)\)"
        bound_enum_matches = re.findall(bound_enum_pattern, self.source_code)
        for bound_enum_match in bound_enum_matches:
            result.append(bound_enum_match)
        return result

    def get_bound_methods(self) -> list[DMethodModel]:
        """

        """
        result: list[DMethodModel] = []
        pattern = r'ClassDB::bind_method\s*\(\s*D_METHOD\(.*?;\s*'
        arg_matches = re.findall(pattern, self.source_code)

        for match in arg_matches:
            d_pattern = r'D_METHOD\(([^)]*)\)'
            arg_matches = re.search(d_pattern, match)
            args = arg_matches.groups(1)
            class_substring = match.split(',')[-1]
            qualified_class_pattern = r"^.*?(?=\))"
            qualified_class_matches = re.search(qualified_class_pattern, class_substring)
            qualified_class = qualified_class_matches.group(0)
            method_model = DMethodModel.from_arg_string(' '.join(args), qualified_class)
            result.append(method_model)
        return result


    def get_bound_properties(self) -> list[PropertyModel]:
        result: list[PropertyModel] = []
        add_property_pattern = r'ADD_PROPERTY\s+\((.*?)\s+\);'
        property_info_pattern = r'PropertyInfo\((.*?)\)'
        property_matches = re.findall(add_property_pattern, self.source_code, re.DOTALL)
        for property_match in property_matches:
            info_match = re.match(property_info_pattern, property_match.lstrip(), re.DOTALL)
            property_info = PropertyInfoModel.from_arg_string(info_match.group(1))
            property_values = re.findall(r'"(.*?)"', property_match)
            bound_property = PropertyModel(field=property_values[0], setter=property_values[2],
                                           getter=property_values[3],
                                           info=property_info)
            result.append(bound_property)
        return result

    def get_bound_signals(self) -> list[MethodInfoModel]:
        """

        """
        result : list[MethodInfoModel] = []

        # hopefully this will fix commented signals from being read
        bound_signal_pattern = r'(?m)^[^\S\r\n]*(?!\/\/)\bADD_SIGNAL\(([\s\S]*?)\);'
        bound_signal_data = re.findall(bound_signal_pattern, self.source_code, re.DOTALL)

        for bound_signal in bound_signal_data:
            name_pattern = r'MethodInfo\(\s*"([^"]+)"'
            signal_name_match = re.match(name_pattern, bound_signal, re.DOTALL)
            signal_name = signal_name_match.group(1)
            property_info_pattern = r'PropertyInfo\s*\(([\s\S]*?)\)'
            property_info_list = re.findall(property_info_pattern, bound_signal)
            parameter_index = 0
            bound_signal_values = MethodInfoModel(name=signal_name)
            for property_info in property_info_list:
                property_cleaned = re.sub(r"//.*", "", property_info.strip())
                parameter_value = PropertyInfoModel.from_arg_string(property_cleaned, parameter_index)
                bound_signal_values.argument_info.append(parameter_value)
                parameter_index += 1
            result.append(bound_signal_values)
        return result


    ###############################################################################
    ##                            Internal                                       ##
    ###############################################################################

    def __init__(self, cpp_file: Path) -> None:
        self.source_file = cpp_file
        """Path: The path to the cpp file with bindings implementation"""
        source_code_original = cpp_file.read_text()
        """The code content of the source file"""
        # Strip block comments (/* ... */)
        clean_code = re.sub(r'/\*.*?\*/', '', source_code_original, flags=re.DOTALL)
        # 2. Strip single-line comments
        clean_code = re.sub(r'//.*$', '', clean_code, flags=re.MULTILINE)
        self.source_code = clean_code


##############################################################################################################
###                                 Data objects                                                           ###
##############################################################################################################
@dataclass(slots=True)
class DMethodModel:
    name: str
    class_name: str
    qualified_name: str
    class_method: str
    args: List[str] = field(default_factory=list)

    @classmethod
    def from_arg_string(cls, arg_string: str, qualified_name: str) -> "DMethodModel":
        args = split_arg_string(arg_string)
        name = args[0]
        method_args = []
        if len(args) > 1:
            for index in range(1, len(args)):
                method_args.append(args[index])
        name_values = qualified_name.split('::')
        clss_name = name_values[0].replace("&",'')
        method_name = name_values[1]
        return cls(name=name, class_name=clss_name, qualified_name=qualified_name, args=method_args,class_method=method_name)



@dataclass(slots=True)
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
    def from_arg_string(cls, arg_string: str) -> "IntegerConstantModel":
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


@dataclass(slots=True)
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


@dataclass(slots=True)
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
    def from_arg_string(cls, arg_string: str, index: int = 0) -> "PropertyInfoModel":
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


@dataclass(slots=True)
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
