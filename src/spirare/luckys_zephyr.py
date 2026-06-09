#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 5/27/26
@File: luckys_zephyr

@Author: Silenuz Nowan (silenuznowan@yahoo.com)

This module contains the LuckyZephyr class that handles loading and parsing the Doxygen generated XML content.
It also contains format information for the mixed element text parser that is part of the class.

Didi: "Tomorrow when I wake or think I do, what shall I say of today?
       That with Estragon my friend, at this place, until the fall of night, I waited for Godot? "
"""
from __future__ import annotations
import copy
import re
from collections import namedtuple
from dataclasses import dataclass, fields, field
from pathlib import Path
from typing import List
from xml.etree import ElementTree as et

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

# track xml tags that should not be parsed, such as htmlonly
element_black_list_set = set()
element_black_list_set.add("htmlonly")
element_black_list_set.add("manonly")
element_black_list_set.add("latexonly")
element_black_list_set.add("xrefsect")


def get_inner_markup(element: et.Element)->str:
    # 1. Grab the initial text chunk before any child tag
    parts = [element.text or ""]
    for child in element:
        # encoding="unicode" returns a standard python string instead of bytes
        parts.append(et.tostring(child, encoding="unicode"))
    return "".join(parts)


def get_data_type(text) -> str:
    """
    Parses text to determine the inner data type for Ref<data> text
    :return: The inner data type for the text
    """
    if text.startswith("Ref<"):
        type_pattern = r"<(.*?)>"
        type_match = re.search(type_pattern, text)
        if type_match:
            return type_match.group(1).strip()
        else:
            return text.strip()
    else:
        return text.strip()


class LuckyZephyr:
    """
    Class to load and parse Doxygen XML for use in generating Godot class
    documentation

    Attributes:
        class_name (str): The name of the class currently loaded
        class_xml (Path): The path to the Doxygen XML file
        data_node (et.Element): The class node of the Doxygen XML file
        reference_file (str): The path to the reference XML file that contains extra information from the header file
        data_xml_map (dict) : Map of each node to it's parent in the form of a dictionary.
        xml_root_node (et.Element): The root node of the Doxygen XML file
    """

    def find_parent_by_child_tag(self,tag:str,value:str)->et.Element:
        node = self.data_node.find(f".//{tag}[.='{value}']")
        if node is not None:
            return self.data_xml_map[node]
        else:
            node = self.reference_node.find(f".//{tag}[.='{value}']")
            if node is not None:
                return self.reference_data_map[node]
            else:
                return None

    def get_bind_methods_implementation(self) -> str:
        """
        Searches the Doxygen XML nodes to find the _bind_methods node,
        if it finds the node it gets the name of the file that has the
        implementation for _bind_methods and returns it
        :return: The name of the source code file that implements _bind_methods
        """
        bind_methods_definition = self.get_member_definition_by_child('name','_bind_methods')
        if bind_methods_definition is not None:
            src_file_name = bind_methods_definition.location.bodyfile
            return src_file_name
        return None

    def get_brief_description(self, doxygen_node: et.Element) -> str:
        """
        Gets the briefdescription tag from the Doxygen element passed as an argument
        and returns the value of the text content.
        :return: The value of the text content
        """
        node = doxygen_node.find('briefdescription')
        text = self.get_tag_text(node)
        return text

    def get_class_brief(self) -> et.Element:
        """
        Creates a brief_description tag with the text content from the Doxygen class documentation's briefdescription
        tag for the class.
        :return: The brief_description tag that was created so it can be added to the Godot XML output
        """
        text = self.get_brief_description(self.data_node)
        brief = et.Element("brief_description")
        brief.text = text
        return brief

    def get_class_detail(self) -> et.Element:
        """
        Creates a description tag with the text content from the Doxygen class documentation's detaileddescription
        tag for the class.
        :return: The description tag that was created so it can be added to the Godot XML output
        """
        text = self.get_detailed_description(self.data_node)
        brief = et.Element("description")
        brief.text = text
        return brief

    def get_detailed_description(self, doxygen_node: et.Element) -> str:
        """
        Gets the detaileddescription tag from the Doxygen element passed as an argument
        and returns the value of the text content.
        :return: The value of the text content
        """
        node = doxygen_node.find('detaileddescription')
        text = self.get_tag_text(node)
        return text

    def get_enumerator_data(self, enumerator_value_name_list: list) -> list[EnumValueModel]:
        """
        Iterates over the list of enumerator value names passed as an argument, it then gets the
        reference file data and node map for the reference file, it then finds each
        enumerator value name in the reference file XML tree, it then uses the parent child
        XML map to get the enumerator-value element, and then the enumerator element from that.
        Lastly it extracts the enumerator information to return to the calling function.
        :param enumerator_value_name_list: List of enumerator value names to search for
        :return: A list of dictionary item containing the extracted information for each enumerator value
        """
        result = []

        doxygen_node = self.reference_node
        enumerator_node_xml_map = self.reference_data_map
        if doxygen_node:
            for enumerator_value in enumerator_value_name_list:
                value_node = self.find_parent_by_child_tag('name', enumerator_value)
                value_definition = self.model_enumvalue_definition(value_node)
                enumerator_node = enumerator_node_xml_map[value_node]
                name_node = enumerator_node.find('name')
                value_definition.enum = name_node.text
                result.append(value_definition)
        return result
        #return self.get_member_definitions(enumerator_value_name_list,'name')

    def get_include_values(self) -> list[str]:
        result = []
        xml_reference_node = self.reference_node
        if xml_reference_node:
            include_node_list = xml_reference_node.findall('.//includes')
            for include_node in include_node_list:
                if include_node.text.startswith('godot_cpp'):
                    include_file_name = Path(include_node.text).name.replace('.hpp', '')
                    class_name = "".join(word.capitalize() for word in include_file_name.split("_"))
                    # handle the fact that 2d or 3d in file name becomes 2D or 3D in Class name
                    actual_class_name = re.sub(r'(?<=\d)(d|D)', lambda match: match.group(0).upper(), class_name)
                    result.append(actual_class_name)
        return result

    def get_method_data(self, method_list: set) -> list[MemberDefinitionModel]:
        """
        Iterates over the list of method names passed as an argument,
        finding each in the current Doxygen XML tree, it then uses the parent child
        XML map to get the parent node which is the main method node, it then extracts method information
        to return to the calling function.
        :param method_list: List of method names to search for
        :return: A list of dictionary item containing the extracted information for each method
        """
        return self.get_member_definitions(method_list,'qualifiedname')

    def get_field_data(self, member_list: list) -> list[MemberDefinitionModel]:
        """
        Iterates over the list of member names passed as an argument,
        finding each in the current Doxygen XML tree, it then uses the parent child
        XML map to get the parent node which is the main member node, it then extracts member information
        to return to the calling function.
        :param member_list: List of member names to search for
        :return: A list of dictionary item containing the extracted information for each member
        """
        return self.get_member_definitions(member_list,'name')

    def get_member_definitions(self,member_list: list,tag_name: str) -> list[MemberDefinitionModel]:
        result = []
        for member in member_list:
            memberdef = self.get_member_definition_by_child(tag_name, member)
            if memberdef is not None:
                result.append(memberdef)
        return result


    def get_member_definition_by_child(self,tag:str,value:str)->MemberDefinitionModel:
        member_def_node = self.find_parent_by_child_tag(tag,value)
        if member_def_node is not None:
            return self.model_member_definition(member_def_node)
        else:
            return None

    def model_enumvalue_definition(self,enum_value_node:et.Element)->EnumValueModel:
        attributes = EnumValueAttributes.from_xml_element(enum_value_node)
        name = enum_value_node.find('name').text
        enum_value_definition = EnumValueModel(name=name,attributes=attributes)
        init_node = enum_value_node.find('initializer')
        if init_node is not None and init_node.text is not None:
            enum_value_definition.initializer = init_node.text
        brief_node = enum_value_node.find('briefdescription')
        if brief_node is not None and brief_node.text is not None:
            content = self.get_tag_text(brief_node)
            enum_value_definition.briefdescription = content
        detail_node = enum_value_node.find('detaileddescription')
        if detail_node is not None and detail_node.text is not None:
            content = self.get_tag_text(detail_node)
            enum_value_definition.detaileddescription = content
        return enum_value_definition



    def model_member_definition(self,member_node:et.Element) -> MemberDefinitionModel:
        attribute_values = MemberDefinitionAttributes.from_xml_element(member_node)
        name_node = member_node.find("name")
        name = name_node.text
        args = dict()
        args['attributes'] = attribute_values
        enum_values : List[EnumValueModel] = list()

        for node in member_node:
            if node.tag == 'detaileddescription':
                if node.text is not None:
                    detailed_description = self.get_tag_text(node)
                    args[node.tag] = detailed_description
            elif node.tag == 'briefdescription':
                if node.text is not None:
                    brief_description = self.get_tag_text(node)
                    args[node.tag] = brief_description
            elif node.tag == 'location':
                args[node.tag] = MemberDefinitionLocation.from_xml_element(node)
            elif node.tag == 'enumvalue':
                enum_value = self.model_enumvalue_definition(node)
                enum_values.append(enum_value)
            elif node.text is not None:
                args[node.tag] = node.text

        member_definition = MemberDefinitionModel.from_dict(args)
        if len(enum_values) > 0:
            member_definition.enum_values = enum_values

        return member_definition

    def get_reference_file_path(self) -> Path:
        """
        Trys to get the absolute path to the reference file containing extra header information.
        :return: Absolute path to the reference file containing extra header information or None if not found
        """
        file_name = self.reference_file + ".xml"
        xml_reference_file = next(Path(self.class_xml.parent).rglob(file_name), None)
        if xml_reference_file:
            return xml_reference_file
        else:
            print("Unable to generate enumerator constants, file not found " + file_name)
            return None

    def get_signal_data(self) -> dict:
        """
        Iterates over the reference items in the Doxygen class XML tree, if a reference item
        is a signal it extracts the information for the signal inserting it in a nested dictionary
        for return to the calling function.  The signal name is the top level key
        :return: a dictionary containing the extracted information for each signal
        """
        reference_nodes = self.data_node.findall(".//xrefsect/..")
        signal_data = dict()
        for reference_node in reference_nodes:
            godot_only_node = reference_node.find(".//godotonly")
            if godot_only_node is not None:
                if godot_only_node.get("kind") == 'signal':
                    signal_name = godot_only_node.get("name")
                    signal_name_actual = re.sub(r"\(.*?\)", "", signal_name)
                    content_nodes = reference_node.findall('.//para')
                    text_node = et.Element('description')
                    text_node.text = content_nodes[2].text
                    for child in content_nodes[2]:
                        text_node.append(copy.deepcopy(child))
                    description = self.parse_xml_text(text_node)
                    signal_values = dict()
                    signal_values['name'] = signal_name_actual
                    signal_values['description'] = description
                    headlines = reference_node.findall('.//simplesect')
                    if len(headlines) > 0:
                        for headline in headlines:
                            if headline.get("kind") == 'note':
                                signal_values['note'] = self.parse_xml_text(headline[0])
                            elif headline.get("kind") == 'warning':
                                signal_values['warning'] = self.parse_xml_text(headline[0])
                    signal_data[signal_name_actual] = signal_values
        return signal_data

    def get_tag_text(self, doxygen_node: et.Element) -> str:
        """
        todo: this docstring is out of date, update it
        central function to get text from a tag.  currently it just strips markup from the text,
        but later can hopefully be used to convert some markup tags in the text to BBCode
        :param doxygen_node: the node to get the text from
        :return: the full content of the text attribute of the doxygen node
        """
        parts = []
        if doxygen_node.text:
            parts.append(doxygen_node.text.strip())
        para_nodes = doxygen_node.findall('para')
        count = len(para_nodes)
        for paragraph_index in range(count):
            paragraph = para_nodes[paragraph_index]
            empty_element = True
            element_text = self.parse_xml_text(paragraph)
            if element_text:
                parts.append(element_text)
                empty_element = False
            if not empty_element and paragraph_index != count - 1:
                parts.append(bbc_linebreak.open)
                parts.append(bbc_linebreak.open)

        text = " ".join(parts)
        return text

    def parse_xml_text(self, doxygen_node: et.Element) -> str:
        parts = []
        has_existing_codeblock = False

        if doxygen_node.tag in element_black_list_set:
            return ""

        if doxygen_node.tag == 'para':
            if len(doxygen_node) > 0:
                if doxygen_node[0].tag == 'xrefsect':
                    return ""

        if doxygen_node.text is not None:
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
                    child_content = self.parse_xml_text(mixed_element_node)
                    parts[-1] = parts[-1] + child_content.strip()
                parts[-1] = parts[-1] + markup.close
            elif mixed_element_node.tag == "godotonly" and mixed_element_node.get("kind") == 'text':

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
            elif mixed_element_node.tag == "programlisting":
                insert_index = len(parts) - 1
                existing_is_godot = True
                if has_existing_codeblock:
                    insert_index = next(i for i, s in enumerate(parts) if s.startswith('[codeblock'))
                    current_codeblock = parts[insert_index]
                    lang_pattern = r'lang=(.*?)\]'
                    lang_value = re.search(lang_pattern, current_codeblock).group(1)
                    current_codeblock = current_codeblock.replace('codeblock lang=', '')
                    current_codeblock = current_codeblock.replace('/codeblock', f'/{lang_value}')
                    parts[insert_index] = current_codeblock
                    if lang_value == 'csharp':
                        existing_is_godot = False

                file_extension = mixed_element_node.get("filename").replace('.', '')
                if file_extension == 'cs':
                    language = 'csharp'
                else:
                    language = file_extension

                block_text = []
                line_nodes = mixed_element_node.findall('codeline')
                for line_node in line_nodes:
                    line = " ".join(line_node.itertext()) + "\n"
                    block_text.append(line)

                if has_existing_codeblock:
                    if existing_is_godot:
                        parts[insert_index] = '[codeblocks]' + parts[insert_index]
                        parts[insert_index] = f'[{language}]]' + "".join(block_text) + f'[/{language}]'
                        parts[insert_index] = parts[insert_index] + '[/codeblocks]'
                    else:
                        current_block = parts[insert_index]
                        parts[insert_index] = f'[codeblocks][{language}]' + "".join(block_text) + f'[/{language}]'
                        parts[insert_index] = parts[insert_index] + current_block + '[/codeblocks]'
                else:
                    parts.append(f'[codeblock lang={language}]' + "".join(block_text) + f'[/codeblock]')

                has_existing_codeblock = True
            else:
                if not mixed_element_node.text is None:
                    parts.append(" ".join(mixed_element_node.itertext()))

            if not mixed_element_node.tail is None and not mixed_element_node.tail == " ":
                if not mixed_element_node.tag == "godotonly":
                    parts.append(mixed_element_node.tail.strip())

        text = " ".join(parts)
        return text

    ###############################################################################
    ##                            Internal                                       ##
    ###############################################################################

    def __init__(self, xml_file: Path) -> None:
        self.class_xml = xml_file
        """Path: The path to the Doxygen XML file"""
        self.data_xml_map = self.__map_xml_nodes()
        """dict:  Map of parent nodes for all child nodes in the Doxygen XML file"""
        self.__set_class_profile()
        self.__load_reference_file()

    def __map_xml_nodes(self) -> dict():
        """
        Sets the xml_root and data_node attributes, and returns a dictionary
        containing a map of nodes where each Doxygen node is mapped to it's parent node
        Why?  That's good question todo: refactor this and just set map here
        """
        tree = et.parse(self.class_xml)
        self.xml_root_node = tree.getroot()
        """et.Element: The root node of the Doxygen XML file"""
        self.data_node = self.xml_root_node[0]
        """et.Element: The class node of the Doxygen XML file"""
        xml_map = {child: parent for parent in self.xml_root_node.iter() for child in parent}
        return xml_map

    def __set_class_profile(self):
        """
        Sets the class_name and reference_ file attributes from values in the Doxygen XML file
        for the current instance.
        """
        class_name = self.data_node.attrib['id']
        self.class_name = class_name.replace("class", "")
        """str: The name of the class currently loaded"""
        reference_node = self.data_node.find('includes')
        self.reference_file = reference_node.attrib['refid']
        """str: The path to the reference XML file that contains extra information from the header file"""

    def __load_reference_file(self):
        reference_file_path = self.get_reference_file_path()
        if reference_file_path:
            tree = et.parse(reference_file_path)
            root = tree.getroot()
            self.reference_node = root[0]
            self.reference_data_map = {child: parent for parent in root.iter() for child in parent}

##################################################################################################################
###                                    Data objects                                                            ###
###################################################################################################################
@dataclass()
class EnumValueAttributes:
    id: str
    prot: str
    @classmethod
    def from_xml_element(cls, member_element:et.Element) -> "EnumValueAttributes":
        attrs = member_element.attrib
        # kind is always present
        kwargs = {"id": attrs["id"], "prot": attrs["prot"]}
        return cls(**kwargs)

@dataclass()
class EnumValueModel:
    attributes: MemberDefinitionAttributes
    name: str
    initializer: str | None = None
    briefdescription: str | None = None
    detaileddescription: str | None = None
    enum: str | None = None
    """Used to store parent enumerator name, not part of doxygen xsd"""

    @property
    def initializer_value(self) -> str:
        return self.initializer.split(" ")[1].strip()


@dataclass
class MemberDefinitionAttributes:
    """
    Data model for Doxygen memberdef element attributes.
    """
    id: str
    """A unique, auto-generated Doxygen identifier string used for cross-referencing throughout the XML structure"""
    kind: str | None = None
    """Specifies the type of member. Common values include: function, variable, typedef, enum, enumvalue, 
    property, or event"""
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
        kwargs = {"id": attrs["id"]}
        # 2. Map everything else dynamically if it exists in the XML
        for xml_key, value in attrs.items():
            if xml_key == "id":
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
    name: str
    """simple name portion of the method or member name"""
    qualifiedname: str | None = None
    """qualified name of the method or member"""
    definition: str | None = None
    """member definition data value followed by qualified name, ex: int Summator::get_total """
    type: str | None = None
    """data type if a field the data type of the field, if a function the return type of the function"""
    briefdescription: str | None = None
    """brief description of the method or member"""
    detaileddescription: str | None = None
    """detailed description of the method or member"""
    initializer: str | None = None
    """for constants and enumerators this indicates the initial value """
    argsstring: str | None = None
    """If applicable contains the argument string for the member"""
    inbodydescription: str | None = None
    alt_description: str | None = None
    location: MemberDefinitionLocation | None = None
    read: str | None = None
    write: str | None = None
    bitfield: str | None = None
    qualifier: str | None = None
    enum_values: List[EnumValueModel] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict):
        valid_fields = {f.name for f in fields(cls)}
        # 2. Filter the input dictionary to keep only valid fields
        filtered_data = {key: value for key, value in data.items() if key in valid_fields}
        # 3. Unpack the filtered dictionary into the class constructor
        return cls(**filtered_data)
