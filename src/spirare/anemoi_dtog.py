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
from xml.etree import ElementTree as et

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
    def from_arg_string(cls, arg_string: str)->"IntegerConstantModel":
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


@dataclass
class MemberDefinitionAttributes:
    """
    Data model for Doxygen memberdef element attributes.
    """
    kind: str
    """Specifies the type of member. Common values include: function, variable, typedef, enum, enumvalue, 
    property, or event"""
    # --- OPTIONAL / CONDITIONAL ATTRIBUTES ---
    # These are initialized via field(default=None) so they can live in any order
    id: str | None = None
    """A unique, auto-generated Doxygen identifier string used for cross-referencing throughout the XML structure"""
    prot: str | None = None
    """The access protection/visibility level in the source code. Possible values: public, protected, private, 
    or package"""
    static: str | None = None
    """Boolean indicator (yes or no) specifying if the member is declared static"""
    const: str | None = None
    """Boolean indicator (yes or no) showing if the member function acts as const"""
    volatile: str | None = None
    """Boolean indicator (yes or no) showing if the member is declared volatile"""
    mutable: str | None = None
    """Boolean indicator (yes or no) for C++ mutable variables"""
    virt: str | None = None
    """Specifies virtual function behavior. Values: non-virtual, virtual, or pure-virtual."""
    explicit: str | None = None
    """Boolean indicator (yes or no) for explicit C++ constructors/conversion operators"""
    inline: str | None = None
    """Boolean indicator (yes or no) indicating if the member was defined inline"""
    final: str | None = None
    sealed: str | None = None
    new: str | None = None
    readable: str | None = None
    writable: str | None = None
    add: str | None = None
    remove: str | None = None
    raise_: str | None = None
    getaccessor: str | None = None
    setaccessor: str | None = None
    accessor: str | None = None
    initonly: str | None = None
    strong: str | None = None

    @classmethod
    def from_xml_element(cls, member_element:et.Element) -> "MemberDefinitionAttributes":
        # get element attributes
        attrs = member_element.attrib
        # kind is always present
        kwargs = {"kind": attrs["kind"]}
        # 2. Map everything else dynamically if it exists in the XML
        for xml_key, value in attrs.items():
            if xml_key == "kind":
                continue
            # Handle Python keyword conflict safely
            if xml_key == "raise":
                kwargs["raise_"] = value
            else:
                kwargs[xml_key] = value

        return cls(**kwargs)


@dataclass()
class MemberDefinitionLocation:
    file: str
    """The path to the source file where the member is defined or declared. 
    This is usually relative to the root input directory unless full paths are enabled in your Doxyfile."""
    line: str
    """The line number in the source file where the member's definition or declaration begins."""
    column: str
    """The column number (character offset) on the line where the member begins.
     (Note: column reporting can be dependent on your specific Doxygen version and configuration)."""
    bodyfile: str | None = None
    """The path to the source file where the actual body (implementation) of the member resides. 
    This is typically used for functions or methods, whereas file denotes where the signature is declared."""
    bodystart: str | None = None
    """The line number where the implementation of the member starts (e.g., the opening brace of a function)."""
    bodyend: str | None = None
    """The line number where the implementation of the member ends (e.g., the closing brace of a function)."""

    @classmethod
    def from_xml_element(cls, location_element: et.Element) -> "MemberDefinitionLocation":
        attrs = location_element.attrib
        kwargs = {"file": attrs["file"]}
        # 2. Map everything else dynamically if it exists in the XML
        for xml_key, value in attrs.items():
            if xml_key == "file":
                continue
            kwargs[xml_key] = value

        return cls(**kwargs)

@dataclass()
class MemberDefinitionModel:
    """
    Used to model data from the Doxygen XML Memberdef elements
    todo: add missing tags, already have more than needed might as well complete it
    """
    attributes: MemberDefinitionAttributes
    location: MemberDefinitionLocation
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
    inbody_description: str | None = None
    alt_description: str | None = None



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
    def from_arg_string(cls, arg_string: str, index: int = 0)->"PropertyInfoModel":
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

