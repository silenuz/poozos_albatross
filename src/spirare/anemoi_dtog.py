#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 6/7/26
@File: anemoi_dtog

@Author: Silenuz Nowan (silenuznowan@yahoo.com)

Contains Data Transfer Objects for Godot
"""
from dataclasses import dataclass
import shlex

def split_arg_string(arg_string: str) -> str:
    lexer = shlex.shlex(arg_string, posix=True)
    lexer.whitespace = ','  # Tell it to split on commas
    lexer.whitespace_split = True  # Only split on whitespace (commas)
    args_list = [arg.strip() for arg in lexer]
    return args_list


@dataclass()
class PropertyInfo:
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

    def get_hint_type(self)->tuple[str, str]:
        # todo: rename soon as possible
        if self.usage_flags is not None:
            if "PROPERTY_USAGE_CLASS_IS_ENUM" in self.usage_flags:
                return 'enum',self.class_name
            else:
                return None
        else:
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
            "class_name" ]
        kwargs = dict(zip(field_names, args))
        kwargs["index"] = index
        return cls(**kwargs)
