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
from collections import namedtuple
import sys
from pathlib import Path
from xml.etree import ElementTree as et
import luckys_zephyr as lz

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

# track bound methods and properties for the current class being processed
bound_methods_set = set()

# track methods that are getters and setters as they should be part of the members output
# and not the methods output
property_methods_set = set()

# track bound enum constants
bound_enums_set = dict()

# track xml tags that should not be parsed, such as htmlonly
element_black_list_set = set()
element_black_list_set.add("htmlonly")
element_black_list_set.add("manonly")
element_black_list_set.add("latexonly")
element_black_list_set.add("xrefsect")

# track property definitions
bound_properties = dict()

# track opening and closing markup for bbcode to translate html markup in element text attibutes
BBCodeMap = namedtuple("BBCodeMap", ["open", "close"])
bbc_bold = BBCodeMap(open="[b]", close=r"[/b]")
bbc_italic = BBCodeMap(open="[i]", close=r"[/i]")
bbc_underline = BBCodeMap(open="[u]", close=r"[/u]")
bbc_strikethrough = BBCodeMap(open="[s]", close=r"[/s]")
bbc_code = BBCodeMap(open="[code]", close=r"[/code]")
bbc_keyboard = BBCodeMap(open="[kbd]", close=r"[/kbd]")
bbc_linebreak = BBCodeMap(open="[br]", close=r"")
bbc_link = BBCodeMap(open="[url]", close=r"[/url]")

format_map = dict()
format_map["bold"] = bbc_bold
format_map["emphasis"] = bbc_italic
format_map["strike"] = bbc_strikethrough
format_map["underline"] = bbc_underline

signal_note_set = set()
signal_warning_set = set()

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


def catalog_bindings(doxygen_data_node: et.Element, class_name: str) -> bool:
    """
    Starts the process of mapping the bindings from the class implementation file that implements
    the _bind_methods function for the class.
    If it gets a name for the implementation it passes to map_godot_bindings function which will
    look for the implementation file.
    :param doxygen_data_node: the doxygen node containing the class data from the doxygen XML file
    :param class_name: the name of the class being parsed
    :return: Success or failure
    """
    # clear_tracked_bindings()
    code_file_name = get_implementation_file_name(doxygen_data_node)
    if code_file_name is None:
        print_message("Unable to determine code implementation file for " + class_name, MESSAGE_TYPE_WARNING)
        return False
    else:
        project_src = src_folder
        code_file = next(project_src.rglob(code_file_name), None)
        if code_file:
            load_godot_bindings(code_file, class_name)
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


def create_bound_enums(bind_method_code: str) -> None:
    """
    Creates the nested dictionary to track enumerator values and the enumerator they belong to.
    :param bind_method_code: The code content of the _bind_methods function
    :return: None
    """
    bound_enum_pattern = r"(?<=BIND_ENUM_CONSTANT)\((.*?)\)"
    bound_enum_matches = re.findall(bound_enum_pattern, bind_method_code)
    for bound_enum_match in bound_enum_matches:
        values = bound_enum_match.split("::")
        enumerator_name = values[0]
        enumerator_value_name = values[1]
        if enumerator_name not in bound_enums_set:
            bound_enums_set[enumerator_name] = dict()
        value_dict = dict()
        value_dict["qualified_name"] = bound_enum_match
        value_dict["enumerator_name"] = enumerator_name
        value_dict["enumerator_value_name"] = enumerator_value_name
        bound_enums_set[enumerator_name][enumerator_value_name] = value_dict


def create_bound_methods(bind_methods_code: str) -> None:
    """
    Creates the bind methods set to track the methods that are bound _bind_methods
    :param bind_methods_code: The code content of the _bind_methods function
    :return: None
    """
    # todo: fix regex so that it doesn't require each declaration starting a line
    bound_method_pattern = r'^\s*ClassDB::.+;'
    bound_methods = re.findall(bound_method_pattern, bind_methods_code, re.MULTILINE)
    for bound_method in bound_methods:
        # get the qualified name of the function from the binding
        definition_match = re.search(r"&([^)]*)\)", bound_method)
        if definition_match:
            qualified_name = definition_match.group(1)
            values = [value for value in qualified_name.split(':') if value]
            name = values[1]
            if not name in property_methods_set:
                bound_methods_set.add(qualified_name)


def create_bound_signals(bind_methods_code: str) -> None:
    bound_signal_pattern = r'ADD_SIGNAL\((.*?)\)\);'
    bound_signals = re.findall(bound_signal_pattern, bind_methods_code)
    for bound_signal in bound_signals:
        print(bound_signal)


def create_enumator_data(godot_root: et.Element, reference: str) -> None:
    """
    Loads the reference file for the Doxygen class XML that is being parsed, if found, then
    the reference file and the Godot XML root element are passed to the enumerator constants preprocessor.
    :param godot_root: The root element of the Godot XML output
    :param reference: The reference file name that was parsed when the Doxygen class XML was first loaded.
    :return: None
    """
    if len(bound_enums_set) < 1:
        return
    file_name = reference + ".xml"
    xml_reference_file = next(Path(xml_input_folder).rglob(file_name), None)
    if xml_reference_file:
        preprocess_enumerator_constants(godot_root, xml_reference_file)
    else:
        print_message("Unable to generate enumerator constants, file not found " + file_name, MESSAGE_TYPE_ERROR)


def get_plain_text_headline(reference_node, mappable_node) -> None:
    reference_string = et.tostring(reference_node, encoding="utf-8").decode("utf-8")
    parts = re.split(r"<godotonly [^>]*/>", reference_string)
    if len(parts) >= 3:
        tail_marked_up = parts[2].replace(f"</{reference_node.tag}>", "")
        plain_tail = re.sub(r"<[^>]+>", "", tail_marked_up)
        signal_note_set.add(plain_tail)
    if len(parts) == 4:
        tail_marked_up = parts[3].replace(f"</{reference_node.tag}>", "")
        plain_tail = re.sub(r"<[^>]+>", "", tail_marked_up)
        signal_note_set.add(plain_tail)


def catalog_reference_headlines(data_node: et.Element) -> None:
    reference_nodes = data_node.findall(".//xrefsect")
    for reference_node in reference_nodes:
        mappable_nodes = reference_node.findall(".//godotonly")
        for mappable_node in mappable_nodes:
            if not mappable_node.get('ref') == 'signal' and 'Note:' in mappable_node.get('content'):
                get_plain_text_headline(reference_node, mappable_node)

    print(signal_note_set)


def create_godot_doc(file: Path) -> None:
    """
    Creates godot XML class documentation from the doxygen XML file whose path is passed as the argument
    :param file: the path to the doxygen XML file that is to be parsed
    :return: None
    """
    class_data = lz.create_profile_for_class(file)
    data_node = class_data[0]
    class_info = class_data[1]
    if catalog_bindings(data_node, class_info.class_name):
        catalog_reference_headlines(data_node)
        godot_root = et.Element('class')
        godot_root.set('name', class_info.class_name)
        set_description(godot_root, data_node)
        create_method_data(godot_root, data_node)
        create_member_data(godot_root, data_node)
        create_enumator_data(godot_root, class_info.reference)
        write_file(godot_root, class_info.class_name)


def create_member_data(godot_root: et.Element, data_node: et.Element) -> None:
    """
    Creates the members node data in the Godot class documentation output
    :param godot_root: the root of the Godot XML output
    :param data_node: the doxygen node containing the class information
    :return: None
    """
    members_node = et.SubElement(godot_root, "members")
    private_attribs = data_node.findall(".//sectiondef[@kind='private-attrib']")
    set_member_data(members_node, private_attribs[0])


def create_method_data(godot_root: et.Element, data_node: et.Element) -> None:
    """
    Retrieves public and protected functions from the doxygen XML so the
    function data can be extracted if it is bound in _bind_methods
    :param godot_root: the root node of the output XML tree
    :param data_node: the class data node from the doxygen XML file
    :return: None
    """
    # create node to add method output data to
    output_methods_node = et.SubElement(godot_root, "methods")

    public_funcs = data_node.findall(".//sectiondef[@kind='public-func']")
    doxygen_methods_node = public_funcs[0]
    set_methods_data(output_methods_node, doxygen_methods_node)
    # todo: add handling of protected functions


def get_class_name(data_node: et.Element) -> lz.ClassInfo:
    # todo: update docstring for new method signature
    """
    Gets the class name from the doxygen node's id attribute
    :param data_node: The doxygen XML node containing the class data
    :return: a string containing the class name
    """
    class_name = data_node.attrib['id']
    name = class_name.replace("class", "")
    reference_node = data_node.find('includes')
    reference = reference_node.attrib['refid']
    return lz.ClassInfo(name, reference)


def get_implementation_file_name(doxygen_data_node: et.Element) -> str:
    """
    Loops through protected static functions looking for the _bind_methods function
    :param doxygen_data_node: the main node containing the class data from the doxygen XML file
    :return: the name of the implementation file in the form of a partial path
    """
    static_funcs = doxygen_data_node.findall(".//sectiondef[@kind='protected-static-func']")
    doxygen_methods_node = static_funcs[0]
    for doxygen_method_node in doxygen_methods_node:
        doxygen_node = doxygen_method_node.find('name')
        if doxygen_node.text == '_bind_methods':
            location_node = doxygen_method_node.find("location")
            src_file_name = location_node.attrib['bodyfile']
            return src_file_name
    return None


def get_property_values(property_match: str) -> dict[str, str]:
    """
    Separates the PropertyInfo from the property_match into separate values for the methods, and backing field
    :param property_match: the PropertyInfo declaration from the _bind_methods function
    :return: A dictionary containing the methods and backing field for the property
    """
    values = re.findall(r'"(.*?)"', property_match)
    property_values = dict()
    property_values["field"] = values[0]
    property_values["setter"] = values[2]
    property_values["getter"] = values[3]
    return property_values


def get_tag_text(doxygen_node: et.Element) -> str:
    """
    central function to get text from a tag.  currently it just strips markup from the text,
    but later can hopefully be used to convert some markup tags in the text to BBCode
    :param doxygen_node: the node to get the text from
    :return: the full content of the text attribute of the doxygen node
    """
    parts = []
    if doxygen_node.text:
        parts.append(doxygen_node.text.strip())

    for mixed_element_node in doxygen_node:
        element_text = parse_xml_text(mixed_element_node)
        parts.append(element_text)
        if mixed_element_node.tag == 'para':
            parts.append(bbc_linebreak.open)
            parts.append(bbc_linebreak.open)

    text = " ".join(parts)

    # todo: fix the above so this is not needed it's pretty ridiculous
    tmp = text.strip()
    while tmp.endswith(bbc_linebreak.open):
        tmp = tmp.removesuffix(bbc_linebreak.open).strip()

    return tmp


def load_godot_bindings(src_file: Path, class_name: str) -> None:
    """
    Parses the implementation code file, to extract the method and property bindings
    :param src_file: the implementation code file for the current class documentation being parsed
    :param class_name: the name of the class for the implementation file
    :return: None
    """
    cpp_file = Path(src_file)
    content = cpp_file.read_text()
    bind_methods_pattern = r"void\s+" + class_name + r"::_bind_methods\(\)\s*\{.*?\}"
    bind_methods_match = re.search(bind_methods_pattern, content, re.DOTALL)

    if bind_methods_match:
        bind_method_content = bind_methods_match.group(0)
        map_godot_bindings(bind_method_content)
    else:
        print_message("_bind_methods function not found in " + src_file, MESSAGE_TYPE_WARNING)


def map_godot_bindings(bind_method_code: str) -> None:
    """
    Adds bound methods, properties and constants from the implementation file to a set, so that the set can be
    checked to see if a method is bound, so only bound methods and properties
    are extracted from the generated doxygen XML.
    :param bind_method_code: The content of the _bind_methods function from opening brace to closing brace
    :return: None
    """
    # get content between opening and closing brace
    bound_methods_match = re.search(r'\{(.*?)\}', bind_method_code, re.DOTALL)
    if bound_methods_match:
        map_property_bindings(bound_methods_match.group(1))
        create_bound_methods(bound_methods_match.group(1))
        create_bound_enums(bound_methods_match.group(1))
        create_bound_signals(bound_methods_match.group(1))
    else:
        print_message("Unknown error could not get content of _bind_methods function", MESSAGE_TYPE_ERROR)


def map_property_bindings(bind_methods_code: str) -> None:
    """
    Maps the property bindings in the _bind_methods function, that are registered using ADD_PROPERTY
    :param bind_methods_code: the code content of the _bind_methods function
    :return: None
    """
    add_property_pattern = r'ADD_PROPERTY\s+\((.*?)\s+\);'
    property_matches = re.findall(add_property_pattern, bind_methods_code, re.DOTALL)
    for property_match in property_matches:
        property_values = get_property_values(property_match)
        field = property_values["field"]
        bound_properties[field] = property_values
        property_methods_set.add(property_values["setter"])
        property_methods_set.add(property_values["getter"])


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


def parse_xml_text(doxygen_node: et.Element) -> str:
    parts = []

    if doxygen_node.tag in element_black_list_set:
        return ""

    if not doxygen_node.text is None:
        parts.append(doxygen_node.text.strip())

    for mixed_element_node in doxygen_node:
        if mixed_element_node.tag in format_map:
            markup = format_map[mixed_element_node.tag]
            if not mixed_element_node.text is None:
                content = markup.open + mixed_element_node.text.strip()
            else:
                content = markup.open
            parts.append(content)
            if len(mixed_element_node):
                child_content = parse_xml_text(mixed_element_node)
                parts[-1] = parts[-1] + child_content.strip()
            parts[-1] = parts[-1] + markup.close
        elif mixed_element_node.tag == "godotonly":

            if mixed_element_node.tail is not None:
                node_tail = mixed_element_node.tail.rstrip()
            else:
                node_tail = ""
            if mixed_element_node.get("content") is not None:
                content = mixed_element_node.get("content")
            else:
                content = ""

            if mixed_element_node.get('position') == "close":
                parts[-1] = parts[-1] + content + node_tail
            else:
                parts.append(content + node_tail)

        if not mixed_element_node.tail is None and not mixed_element_node.tail == " ":
            if not mixed_element_node.tag == "godotonly":
                parts.append(mixed_element_node.tail.strip())

    text = " ".join(parts)
    return text


def preprocess_enumerator_constants(godot_root: et.Element, xml_reference_file: Path) -> None:
    """
    Finds the enumerator section in the reference file, once found it loops through each enumerator
    checking to see if the enumerator is bound, if so it calls set_enumerator_data which will add the
    bound enum values to the Godot output XML
    :param godot_root: The root element of the Godot output XML
    :param xml_reference_file: the reference file path for the Doxygen output
    :return: None
    """
    tree = et.parse(xml_reference_file)
    root = tree.getroot()
    enum_nodes = root.findall(".//sectiondef[@kind='enum']")
    for enumerator_node in enum_nodes[0]:
        enumerator_name_node = enumerator_node.find('name')
        value_name = enumerator_name_node.text
        if value_name in bound_enums_set:
            set_enumerator_data(godot_root, enumerator_node, value_name)


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


def set_brief_description(godot_node: et.Element, data_node: et.Element) -> None:
    """
    Gets the brief description from the doxygen node's briefdescription tag
    and adds it as the brief_description node to the Godot XML node.
    :param godot_node: The Godot XML node to add the brief_description tag to
    :param data_node: The doxygen XML node to search for the briefdescription tag.
    :return: None
    """
    node = data_node.find('briefdescription')
    text = get_tag_text(node)
    brief = et.SubElement(godot_node, "brief_description")
    brief.text = text


def set_description(godot_node: et.Element, data_node: et.Element) -> None:
    """
    Adds brief_description and description tags to the Godot XML node
    after finding the data in the doxygen data node
    :param godot_node: the Godot XML node to add the tags to
    :param data_node: The doxygen XML node to search for the tags.
    :return: None
    """
    set_brief_description(godot_node, data_node)
    set_detailed_description(godot_node, data_node)


def set_detailed_description(godot_node: et.Element, data_node: et.Element) -> None:
    """
    Adds description tags to the Godot XML node after looking it up in the doxygen XML node
    :param godot_node: The Godot XML node to add the description tag to
    :param data_node: The doxygen node to search for the detaileddescription tag.
    :return: None
    """
    node = data_node.find("detaileddescription")
    text = get_tag_text(node)
    detailed = et.SubElement(godot_node, "description")
    detailed.text = text


def set_detailed_description_as_text(godot_node: et.Element, data_node: et.Element) -> None:
    """
    Adds description tags to the Godot XML node after looking it up in the doxygen XML node
    :param godot_node: The Godot XML node to add the description tag to
    :param data_node: The doxygen node to search for the detaileddescription tag.
    :return: None
    """
    node = data_node.find("detaileddescription")
    text = get_tag_text(node)
    godot_node.text = text


def set_enumerator_data(godot_root: et.Element, enumerator_node: et.Element, enumerator_name: str) -> None:
    """
    Loops through the elements in the Doxygen enumerator element to find the enumerator values.  For each enumerator value it
    checks if it is bound, if it is it is output to the constants node of the Godot output XML
    :param godot_root: The root element of the Godot XML output
    :param enumerator_node: The enumerator element from the Doxygen XML reference file
    :param enumerator_name: The name of the enumerator
    :return: None
    """
    constants_node = add_constants_node(godot_root)
    # track index, Godot will pick up the values after the last initialized value based on index.
    index_value = 0

    for enumerator_value_node in enumerator_node:
        if enumerator_value_node.tag == "enumvalue":
            enumerator_value_name_node = enumerator_value_node.find('name')
            enumerator_value_name = enumerator_value_name_node.text
            if enumerator_value_name in bound_enums_set[enumerator_name]:
                output_values = bound_enums_set[enumerator_name][enumerator_value_name]
                output_node = et.SubElement(constants_node, "constant")
                output_node.set("name", output_values["qualified_name"])
                output_node.set("enum", output_values["enumerator_name"])
                initial_value_node = enumerator_value_node.find("initializer")
                if initial_value_node is not None:
                    text_content = initial_value_node.text
                    value = text_content.split(" ")[1].strip()
                    index_value = int(value)
                output_node.set("value", str(index_value))
                set_detailed_description_as_text(output_node, enumerator_value_node)
                index_value += 1


def set_member_data(godot_members_node: et.Element, doxygen_node: et.Element) -> None:
    """
    loops through all the private fields defined in the doxygen XML and find the fields corresponding
    to backing fields of the bound properties
    :param godot_members_node: the members node in the Godot output XML
    :param doxygen_node: the doxygen XML node containing the field information
    :return: None
    """
    for doxygen_member_node in doxygen_node:
        name_node = doxygen_member_node.find("name")
        if name_node.text in bound_properties:
            property_values = bound_properties[name_node.text]
            output_member_node = et.SubElement(godot_members_node, "member")
            output_member_node.set("name", name_node.text)
            output_member_node.set("setter", property_values["setter"])
            output_member_node.set("getter", property_values["getter"])
            type_node = doxygen_member_node.find("type")
            type_value = type_node.text
            if type_value.startswith("Ref<"):
                type_pattern = r"<(.*?)>"
                type_match = re.search(type_pattern, type_value)
                if type_match:
                    output_member_node.set("type", type_match.group(1).strip())
            else:
                output_member_node.set("type", type_value)
            description_node = doxygen_member_node.find("detaileddescription")
            if description_node is not None:
                output_member_node.text = get_tag_text(description_node)


def set_method_data(output_methods_node: et.Element, doxygen_method_node: et.Element) -> None:
    """
    extracts data from the method node in the doxygen XML file, and creates a node
    in the output class docs XML methods node.
    :param output_methods_node: the output (Godot) XML node named methods
    :param doxygen_method_node: the method node from doxygen to extract data from
    :return: None
    """
    doxygen_node = doxygen_method_node.find('name')
    method = et.SubElement(output_methods_node, "method")
    method.set('name', doxygen_node.text)
    set_detailed_description(method, doxygen_method_node)
    doxygen_node = doxygen_method_node.find('type')
    return_type = et.SubElement(method, "return")
    if doxygen_node.text:
        return_value_type = doxygen_node.text
    else:
        return_value_type = "void"
    return_type.set('type', return_value_type)


def set_methods_data(output_methods_node: et.Element, doxygen_methods_node: et.Element) -> None:
    """
    Mostly acts a gatekeeper, this function loops through the methods in the doxygen methods node
    if the function is mapped as being bound in _bind_methods, the node is passed to add_method_data
    to actually add the data to the output XML
    :param output_methods_node: the output (Godot) XML node named methods
    :param doxygen_methods_node: the doxygen methods node containing the methods and their descriptions
    :return: None
    """
    for doxygen_method_node in doxygen_methods_node:
        qualified_name_node = doxygen_method_node.find("qualifiedname")
        if qualified_name_node.text in bound_methods_set:
            set_method_data(output_methods_node, doxygen_method_node)


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
