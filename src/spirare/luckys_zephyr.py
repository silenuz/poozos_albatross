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
import copy
import html
import re
from collections import namedtuple
from pathlib import Path
from xml.etree import ElementTree as et

from src.spirare.anemoi_dtog import MemberDefinitionModel

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


# element_black_list_set.add("programlisting")

class LuckyZephyr:
    """
    Class to load and parse Doxygen XML for use in generating Godot class
    documentation

    Attributes:
        class_name (str): The name of the class currently loaded
        class_xml (Path): The path to the Doxygen XML file
        data_node (et.Element): The class node of the Doxygen XML file
        reference_file (str): The path to the reference XML file that contains extra information from the header file
        xml_map (dict) : Map of each node to it's parent in the form of a dictionary.
        xml_root_node (et.Element): The root node of the Doxygen XML file
    """

    def get_bind_methods_implementation(self) -> str:
        """
        Searches the Doxygen XML nodes to find the _bind_methods node,
        if it finds the node it gets the name of the file that has the
        implementation for _bind_methods and returns it
        :return: The name of the source code file that implements _bind_methods
        """
        bind_methods_node = self.data_node.find(".//name[.='_bind_methods']")
        if bind_methods_node is not None:
            definition_node = self.xml_map[bind_methods_node]
            location_node = definition_node.find("location")
            src_file_name = location_node.attrib['bodyfile']
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

    def get_data_type(self, text) -> str:
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
            return text

    def get_detailed_description(self, doxygen_node: et.Element) -> str:
        """
        Gets the detaileddescription tag from the Doxygen element passed as an argument
        and returns the value of the text content.
        :return: The value of the text content
        """
        node = doxygen_node.find('detaileddescription')
        text = self.get_tag_text(node)
        return text

    def get_enumerator_data(self, enumerator_value_name_list: list) -> list[dict]:
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
        enumerator_data = self.load_reference_file()
        doxygen_node = enumerator_data[0]
        enumerator_node_xml_map = enumerator_data[1]

        if doxygen_node:
            for enumerator_value in enumerator_value_name_list:
                value_name_node = doxygen_node.find(f".//name[.='{enumerator_value}']")
                enumerator_value_node = enumerator_node_xml_map[value_name_node]
                enumerator_node = enumerator_node_xml_map[enumerator_value_node]
                name_node = enumerator_node.find('name')
                enumerator_name = name_node.text
                description = self.get_detailed_description(enumerator_value_node)
                enumerator_definition = dict()
                enumerator_definition['name'] = enumerator_value
                enumerator_definition['description'] = description
                enumerator_definition['enumerator_name'] = enumerator_name
                initial_value_node = enumerator_value_node.find("initializer")
                if initial_value_node is not None:
                    initial_value = initial_value_node.text.split(" ")[1].strip()
                    enumerator_definition['initial_value'] = initial_value
                result.append(enumerator_definition)

        return result

    def get_include_values(self) -> list[str]:
        result = []
        reference_file_content = self.load_reference_file()
        xml_reference_node = reference_file_content[0]
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

    def get_method_data(self, method_list: set) -> list[dict]:
        """
        Iterates over the list of method names passed as an argument,
        finding each in the current Doxygen XML tree, it then uses the parent child
        XML map to get the parent node which is the main method node, it then extracts method information
        to return to the calling function.
        :param method_list: List of method names to search for
        :return: A list of dictionary item containing the extracted information for each method
        """
        result: list[dict] = []
        for method in method_list:
            name_node = self.data_node.find(f".//qualifiedname[.='{method}']")
            if name_node is not None:
                method_node = self.xml_map[name_node]
                name_node = method_node.find("name")
                name = name_node.text
                description = self.get_detailed_description(method_node)
                doxygen_type_node = method_node.find('type')
                if doxygen_type_node.text:
                    return_value_type = doxygen_type_node.text
                else:
                    return_value_type = "void"
                method_data = dict()
                method_data["name"] = name
                method_data["description"] = description
                method_data["return_type"] = return_value_type
                result.append(method_data)

        return result

    def get_member_data(self, member_list: list) -> list[MemberDefinitionModel]:
        """
        Iterates over the list of member names passed as an argument,
        finding each in the current Doxygen XML tree, it then uses the parent child
        XML map to get the parent node which is the main member node, it then extracts member information
        to return to the calling function.
        :param member_list: List of member names to search for
        :return: A list of dictionary item containing the extracted information for each member
        """
        result = []
        for member in member_list:
            name_node = self.data_node.find(f".//name[.='{member}']")
            if name_node is not None:
                name = name_node.text
                member_node = self.xml_map[name_node]
                type_node = member_node.find("type")
                type_value = self.get_data_type(type_node.text)
                definition_node = member_node.find("definition")
                definition_value = definition_node.text
                qualified_name_node = member_node.find("qualifiedname")
                qualified_name_value = qualified_name_node.text
                member_values = MemberDefinitionModel(
                    member_type=type_value,
                    definition=definition_value,
                    member_name=name,
                    qualified_name=qualified_name_value,
                )
                description_node = member_node.find("detaileddescription")
                if description_node.text is not None:
                    member_values.description = self.get_tag_text(description_node)

                initializer_node = member_node.find("initializer")
                if initializer_node is not None and initializer_node.text is not None:
                   member_values.initializer = initializer_node.text

                argg_node = member_node.find("argsstring")
                if argg_node.text is not None:
                   member_values.arg_string = argg_node.text

                result.append(member_values)
        return result

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

    def load_reference_file(self) -> tuple[et.Element, dict]:
        reference_file_path = self.get_reference_file_path()
        if reference_file_path:
            tree = et.parse(reference_file_path)
            root = tree.getroot()
            xml_map = {child: parent for parent in root.iter() for child in parent}
            return root, xml_map
        else:
            return None, None

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
        self.xml_map = self.__map_xml_nodes()
        """dict:  Map of parent nodes for all child nodes in the Doxygen XML file"""
        self.__set_class_profile()

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
