#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 5/27/26
@File: aerify_didi

@Author: Silenuz Nowan (silenuznowan@yahoo.com)

This module parses Doxygen XML output to generate Godot class documentation for a GDExtension.

Command-line Arguments:

Didi: "Well? What do we do?"
Gogo: "Don't let's do anything.  It's safer"
"""
import re
import importlib.util
import sys
from pathlib import Path
from xml.etree import ElementTree as et
from luckys_zephyr import LuckyZephyr
from src.spirare.anemoi_dtog import PropertyInfoModel, PropertyModel, MethodInfoModel, IntegerConstantModel, PoozoNotus, \
    DMethodModel

xml_input_folder = sys.argv[1]
dest_folder = sys.argv[2]
src_folder = Path(dest_folder).parent

template_methods_path = next(src_folder.rglob("methods.py"), None)
module_name = "template_methods"
template_methods_found = False
methods_module = None

if template_methods_path is not None:
    try:
        # try importing methods.py from the template build process so we can use colored printing
        spec = importlib.util.spec_from_file_location(module_name, template_methods_path)
        methods_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(methods_module)
        template_methods_found = True
    except Exception as e:
        print(f"Error during import: {e}")
else:
    print("methods.py not found")

# track bound enum constants
bound_enums_set = []

# track bound methods and properties for the current class being processed
bound_methods_set : dict[str,DMethodModel] = {}

# track property definitions
bound_properties: dict[str, PropertyModel] = {}

# track bound signals
bound_signals: dict[str, MethodInfoModel] = {}

bound_constants: dict[str, IntegerConstantModel] = {}

# track methods that are getters and setters as they should be part of the members output
# and not the methods output
property_methods_set = set()

MESSAGE_TYPE_WARNING = 0
MESSAGE_TYPE_ERROR = 1


def add_constants_node(godot_root: et.Element) -> et.Element:
    """
    Get the constants element from the Godot output XML, if it doesn't exist it create one
    :param godot_root: The Godot root element of the output XML
    :return: The constants element from the Godot output XML
    """
    constants_node = godot_root.find("constants")
    if not constants_node is None:
        return constants_node
    else:
        constants_node = et.SubElement(godot_root, "constants")
        return constants_node


def catalog_bindings(lz_data: LuckyZephyr) -> bool:
    """
    Starts the process of mapping the bindings from the class implementation file that implements
    the _bind_methods function for the class.
    If it gets a name for the implementation it passes to map_godot_bindings function which will
    look for the implementation file.
    :param lz_data: instance of LuckyZephyr containing the current Doxygen class XML file
    :return: Success or failure
    """
    # clear_tracked_bindings()
    code_file_name = lz_data.get_bind_methods_implementation()
    if code_file_name is None:
        print_message("Unable to determine code implementation file for " + lz_data.class_name, MESSAGE_TYPE_WARNING)
        return False
    else:
        project_src = src_folder
        code_file = next(project_src.rglob(code_file_name), None)
        if code_file:
            poozo_data = PoozoNotus(code_file)
            load_godot_bindings(poozo_data, lz_data.class_name)
            return True
        else:
            print_message("Code Implementation File not found " + code_file_name, MESSAGE_TYPE_ERROR)
            return False


def clear_tracked_bindings() -> None:
    """
    Clears all tracked bindings for methods, properties, etc..
    :return: None
    """
    bound_methods_set.clear()
    property_methods_set.clear()
    bound_properties.clear()
    bound_enums_set.clear()
    bound_signals.clear()


def create_bound_constants(poozo_data:PoozoNotus, class_name: str) -> None:
    constants = poozo_data.get_bound_constants(class_name)
    for constant_info in constants:
        bound_constants[constant_info.p_name] = constant_info


def create_bound_enums(poozo_data:PoozoNotus) -> None:
    """

    """
    enums = poozo_data.get_bound_enums()
    bound_enums_set.extend(enums)

def create_bound_methods(poozo_data:PoozoNotus) -> None:
    """

    """
    methods = poozo_data.get_bound_methods()
    for method_info in methods:
        if not method_info.name in property_methods_set:
            bound_methods_set[method_info.qualified_name] = method_info

def create_bound_properties(poozo_data: PoozoNotus) -> None:
    """
    Maps the property bindings in the _bind_methods function, that are registered using ADD_PROPERTY

    """
    properties = poozo_data.get_bound_properties()
    for bound_property in properties:
        bound_properties[bound_property.field] = bound_property
        property_methods_set.add(bound_property.getter)
        property_methods_set.add(bound_property.setter)

def create_bound_signals(poozo_data:PoozoNotus) -> None:
    """

    """
    signals = poozo_data.get_bound_signals()
    for signal in signals:
        bound_signals[signal.name] = signal


def set_constants_data(godot_root: et.Element, lucky_data: LuckyZephyr) -> None:
    output_constants_node = add_constants_node(godot_root)
    for integer_constant in bound_constants:
        pass


def create_godot_doc(file: Path) -> None:
    """
    Creates godot XML class documentation from the doxygen XML file whose path is passed as the argument
    :param file: the path to the doxygen XML file that is to be parsed
    :return: None
    """
    lucky = LuckyZephyr(file)
    if catalog_bindings(lucky):
        godot_root = et.Element('class')
        godot_root.set('name', lucky.class_name)
        godot_root.append(lucky.get_class_brief())
        godot_root.append(lucky.get_class_detail())
        set_method_data(godot_root, lucky)
        set_member_data(godot_root, lucky)
        set_enumerator_data(godot_root, lucky)
        set_signal_data(godot_root, lucky)
        set_constants_data(godot_root, lucky)
        write_file(godot_root, lucky.class_name)


def load_godot_bindings(poozo_data: PoozoNotus, class_name: str) -> None:
    """

    """
    create_bound_properties(poozo_data)
    create_bound_methods(poozo_data)
    create_bound_enums(poozo_data)
    create_bound_signals(poozo_data)
    create_bound_constants(poozo_data, class_name)


def parse_class_xml_files() -> None:
    """
    loop through the class documentation files generated by doxygen and
    create a Godot class document file for each
    :return: None
    """
    files = list(Path(xml_input_folder).rglob('class*.xml'))
    for file in files:
        clear_tracked_bindings()
        create_godot_doc(file)


def print_message(message: str, message_type: int) -> None:
    """
    Prints output messages, if methods.py from the cpp template is found it uses the color printing from that
    module.
    :param message: The message to print
    :param message_type: The type of message, warning or error
    :return: None
    """
    if template_methods_found:
        if message_type == MESSAGE_TYPE_ERROR:
            methods_module.print_error(message)
        elif message_type == MESSAGE_TYPE_WARNING:
            methods_module.print_warning(message)
        else:
            print(message)
    else:
        print(message)


def set_enumerator_data(godot_root: et.Element, lz_data: LuckyZephyr) -> None:
    """
    Loops through the elements in the Doxygen enumerator element to find the enumerator values.  For each enumerator value it
    checks if it is bound, if it is it is output to the constants node of the Godot output XML
    :param godot_root: The root element of the Godot XML output
    :param lz_data: The LuckyZephyr instance with the current doxygen class data
    :return: None
    """
    constants_node = add_constants_node(godot_root)
    enumerator_value_names = list(dict.fromkeys(bound_enums_set))
    enumerator_value_data = lz_data.get_enumerator_data(enumerator_value_names)

    # track index, Godot will pick up the values after the last initialized value based on index.
    index_value = 0
    for enumerator_value in enumerator_value_data:
        description = enumerator_value.detaileddescription
        output_node = et.SubElement(constants_node, "constant")
        output_node.set("name", enumerator_value.name)
        output_node.set("enum", enumerator_value.enum)
        if enumerator_value.initializer is not None:
            value = enumerator_value.initializer_value
            index_value = int(value)
        output_node.set("value", str(index_value))
        output_node.text = description
        index_value += 1


def set_member_data(godot_root_node: et.Element, lz_data: LuckyZephyr) -> None:
    """
    loops through all the private fields defined in the doxygen XML and find the fields corresponding
    to backing fields of the bound properties
    :param godot_root_node: the root node in the Godot output XML
    :param lz_data: The LuckyZephyr instance with the current doxygen class data
    :return: None    """

    properties = list(bound_properties)
    member_data = lz_data.get_field_data(properties)
    members_node = et.SubElement(godot_root_node, "members")

    for member in member_data:
        bound_property = bound_properties[member.name]
        output_member_node = et.SubElement(members_node, "member")
        output_member_node.set("name", member.name)
        output_member_node.set("setter", bound_property.setter)
        output_member_node.set("getter", bound_property.getter)
        output_member_node.set("type", bound_property.info.variant_type_name)
        hint_type = bound_property.info.get_hint_type()
        if hint_type is not None:
            if hint_type[1] is None:
                output_member_node.set(hint_type[0], member.type)
            else:
                output_member_node.set(hint_type[0], hint_type[1])

        if member.detaileddescription:
            output_member_node.text = member.detaileddescription


def set_method_data(godot_root_node: et.Element, lz_data: LuckyZephyr) -> None:
    """
    extracts data from the method node in the doxygen XML file, and creates a node
    in the output class docs XML methods node.
    :param godot_root_node: The root element of the Godot XML output
    :param lz_data: The LuckyZephyr instance with the current doxygen class data
    :return: None
    """
    method_data = lz_data.get_method_data(bound_methods_set)
    methods_node = et.SubElement(godot_root_node, "methods")
    for method in method_data:
        output_method_node = et.SubElement(methods_node, "method")
        output_method_node.set("name", method.name)
        if method.detaileddescription:
            output_method_node_description = et.SubElement(output_method_node, "description")
            output_method_node_description.text = method.detaileddescription
        output_method_node_return = et.SubElement(output_method_node, "return")
        output_method_node_return.set("type", method.type)


def set_signal_data(godot_root: et.Element, lz_data: LuckyZephyr):
    """
    Sets the signal data in the Godot output XML
    :param godot_root: godot root element to add signal data to
    :param lz_data: LuckyZephyr instance with the current doxygen class XML
    """
    if len(bound_signals) < 1:
        return

    signal_data = lz_data.get_signal_data()
    signals_node = et.SubElement(godot_root, "signals")
    # first generate the standard skeleton output doctool would create for signals
    for signal in bound_signals:
        signal_node = et.SubElement(signals_node, "signal")
        signal_node.set("name", signal)
        parameters = bound_signals[signal].argument_info
        if len(parameters) > 0:
            for bound_parameter in parameters:
                parameter_node = et.SubElement(signal_node, "parameter")
                parameter_node.set("index", bound_parameter.index_string)
                parameter_node.set("name", bound_parameter.name)
                parameter_node.set("type", bound_parameter.variant_type_name)
                specified_type = bound_parameter.get_hint_type()
                if specified_type is not None:
                    parameter_node.set(specified_type[0], specified_type[1])
        # if the signal has a description and or notes add them
        if signal in signal_data:
            description_node = et.SubElement(signal_node, "description")
            description = signal_data[signal]['description']
            if 'note' in signal_data[signal]:
                description = description + '[br][br][b]Note:[/b]' + ' ' + signal_data[signal]['note']
            if 'warning' in signal_data[signal]:
                description = description + '[br][br][b]Warning:[/b]' + ' ' + signal_data[signal]['warning']
            description_node.text = description


def write_file(godot_root: et.Element, class_name: str) -> bool:
    """
    Writes the Godot XML tree to the output file
    :param godot_root: The root node of the Godot XML tree
    :param class_name: The name of the class, used for the file name
    :return: Success or failure
    """
    result = False
    et.indent(godot_root, space="  ", level=0)
    tree = et.ElementTree(godot_root)
    file_name = dest_folder + "/" + class_name + ".xml"

    Path(dest_folder).mkdir(parents=True, exist_ok=True)

    try:
        tree.write(file_name, encoding="utf-8", xml_declaration=True, short_empty_elements=False)
        result = True
    except(OSError, IOError) as e:
        # Catches issues like permission denied or invalid paths
        print_message(f"File system error: {e}", MESSAGE_TYPE_ERROR)
    except Exception as e:
        # Catches other potential issues (e.g., non-serializable data)
        print_message(f"An unexpected error occurred: {e}", MESSAGE_TYPE_ERROR)

    return result


if __name__ == '__main__':
    parse_class_xml_files()
