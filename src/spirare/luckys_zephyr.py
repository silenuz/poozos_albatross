#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 5/27/26
@File: luckys_zephyr

@Author: Silenuz Nowan (silenuznowan@yahoo.com)

This module contains the LuckyZephyr class that handles loading and parsing the Doxygen generated XML content.

Didi: "Tomorrow when I wake or think I do, what shall I say of today?
       That with Estragon my friend, at this place, until the fall of night, I waited for Godot? "
"""
from __future__ import annotations
import re
from dataclasses import dataclass, fields, field
from pathlib import Path
from typing import List
from xml.etree import ElementTree as et


def get_inner_markup(element: et.Element) -> str:
    # 1. Grab the initial text chunk before any child tag
    parts = [element.text or ""]
    for child in element:
        # encoding="unicode" returns a standard python string instead of bytes
        parts.append(et.tostring(child, encoding="unicode"))
    return "".join(parts).strip()


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
    def find_node_by_search_value(self,search: str)->et.Element:
        node = self.data_node.find(search)
        if node is not None:
            return self.data_xml_map[node]
        else:
            node = self.reference_node.find(search)
            if node is not None:
                return self.reference_data_map[node]
            else:
                return None

    def find_by_child_attr(self, attribute_name: str, value: str) -> et.Element:
        return self.find_node_by_search_value(f".//*[@{attribute_name}='{value}']")


    def find_by_child_tag(self, tag: str, value: str) -> et.Element:
        return self.find_node_by_search_value(f".//{tag}[.='{value}']")


    def get_class_description(self, node_name: str) -> str:
        node = self.data_node.find(node_name)
        if node.text is not None:
            brief_description = get_inner_markup(node)
            return brief_description
        else:
            return None

    def get_class_brief(self) -> str:
        """
        Creates a brief_description tag with the text content from the Doxygen class documentation's briefdescription
        tag for the class.
        :return: The brief_description tag that was created so it can be added to the Godot XML output
        """
        return self.get_class_description("briefdescription")

    def get_class_detail(self) -> str:
        """
        Creates a description tag with the text content from the Doxygen class documentation's detaileddescription
        tag for the class.
        :return: The description tag that was created so it can be added to the Godot XML output
        """
        return self.get_class_description("detaileddescription")

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

        if doxygen_node:
            for enumerator_value in enumerator_value_name_list:
                value_definition = self.get_enumerator_value(enumerator_value)
                result.append(value_definition)
        return result
        # return self.get_member_definitions(enumerator_value_name_list,'name')


    def get_enumerator_value(self, enumerator_value_name: str)->EnumValueModel:
        enumerator_node_xml_map = self.reference_data_map
        value_node = self.find_by_child_tag('name', enumerator_value_name)
        value_definition = self.model_enumvalue_definition(value_node)
        enumerator_node = enumerator_node_xml_map[value_node]
        name_node = enumerator_node.find('name')
        value_definition.enum = name_node.text
        return value_definition


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
        return self.get_member_definitions(method_list, 'qualifiedname')

    def get_field_data(self, member_list: list) -> list[MemberDefinitionModel]:
        """
        Iterates over the list of member names passed as an argument,
        finding each in the current Doxygen XML tree, it then uses the parent child
        XML map to get the parent node which is the main member node, it then extracts member information
        to return to the calling function.
        :param member_list: List of member names to search for
        :return: A list of dictionary item containing the extracted information for each member
        """
        return self.get_member_definitions(member_list, 'name')

    def get_member_definitions(self, member_list: list, tag_name: str) -> list[MemberDefinitionModel]:
        result = []
        for member in member_list:
            memberdef = self.get_definition_by_tag(tag_name, member)
            if memberdef is not None:
                result.append(memberdef)
        return result

    def get_definition_by_tag(self, tag: str, value: str) -> MemberDefinitionModel:
        member_def_node = self.find_by_child_tag(tag, value)
        if member_def_node is not None:
            return self.model_member_definition(member_def_node)
        else:
            return None

    @staticmethod
    def model_enumvalue_definition(enum_value_node: et.Element) -> EnumValueModel:
        attributes = EnumValueAttributes.from_xml_element(enum_value_node)
        name = enum_value_node.find('name').text
        enum_value_definition = EnumValueModel(name=name, attributes=attributes)
        init_node = enum_value_node.find('initializer')
        if init_node is not None and init_node.text is not None:
            enum_value_definition.initializer = init_node.text
        brief_node = enum_value_node.find('briefdescription')
        if brief_node is not None and brief_node.text is not None:
            content = get_inner_markup(brief_node)
            enum_value_definition.briefdescription = content
        detail_node = enum_value_node.find('detaileddescription')
        if detail_node is not None and detail_node.text is not None:
            content = get_inner_markup(detail_node)
            enum_value_definition.detaileddescription = content
        return enum_value_definition

    @staticmethod
    def model_member_definition(member_node: et.Element) -> MemberDefinitionModel:
        attribute_values = MemberDefinitionAttributes.from_xml_element(member_node)
        name_node = member_node.find("name")
        name = name_node.text
        args = dict()
        args['attributes'] = attribute_values
        enum_values: List[EnumValueModel] = list()
        param_values: List[ParameterTypeModel] = list()

        for node in member_node:
            if node.tag == 'detaileddescription':
                if node.text is not None:
                    detailed_description = get_inner_markup(node)
                    args[node.tag] = detailed_description
            elif node.tag == 'briefdescription':
                if node.text is not None:
                    brief_description = get_inner_markup(node)
                    args[node.tag] = brief_description
            elif node.tag == 'location':
                args[node.tag] = MemberDefinitionLocation.from_xml_element(node)
            elif node.tag == 'enumvalue':
                enum_value = LuckyZephyr.model_enumvalue_definition(node)
                enum_values.append(enum_value)
            elif node.tag == 'param':
                parameter = LuckyZephyr.model_param_definition(node)
                param_values.append(parameter)
            elif node.text is not None:
                args[node.tag] = node.text

        member_definition = MemberDefinitionModel.from_dict(args)
        if len(enum_values) > 0:
            member_definition.enum_values = enum_values
        if len(param_values) > 0:
            member_definition.parameters = param_values
        return member_definition


    @staticmethod
    def model_param_definition(node)->ParameterTypeModel:
        values = dict()
        for element in node:
            if element.text is not None:
                values[element.tag] = element.text
        model = ParameterTypeModel(**values)
        return model


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


    def get_xref_items(self,title: str)->list[XRefSectionModel]:
        reference_nodes = self.data_node.findall(f".//xrefsect/[xreftitle='{title}']")
        result: list[XRefSectionModel] = []
        for reference_node in reference_nodes:
            xrefitem = XRefSectionModel.from_xml(reference_node)
            result.append(xrefitem)
        return result

    def get_headlines_for_xrefitem(self,refitem: XRefSectionModel)->list[SimpleSectionModel]:
        result: list[SimpleSectionModel] = []
        parent_node = self.find_by_child_attr('id',refitem.id)
        if parent_node is not None and parent_node.tag == 'para':
            headline_nodes = parent_node.findall("simplesect")
            for headline_node in headline_nodes:
                headline = SimpleSectionModel.from_xml(headline_node)
                result.append(headline)
        return result

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
                    signal_description = reference_node.find(".//parblock")
                    signal_paras = signal_description.findall("para")
                    desc_paragraphs = signal_paras[1:]

                    description_paragraphs : list[str] = list()
                    for desc in desc_paragraphs:
                        desc_string = get_inner_markup(desc)
                        description_paragraphs.append(desc_string)

                    if len(description_paragraphs) > 0:
                        description = " ".join(description_paragraphs)
                    else:
                        description = None

                    signal_values = dict()
                    signal_values['name'] = signal_name_actual
                    if description is not None:
                        signal_values['description'] = f'<desc>{description}</desc>'
                        headlines = reference_node.findall('.//simplesect')
                    if len(headlines) > 0:
                        for headline in headlines:
                            if headline.get("kind") == 'note':
                                signal_values['note'] = get_inner_markup(headline)
                            elif headline.get("kind") == 'warning':
                                signal_values['warning'] = get_inner_markup(headline)
                    signal_data[signal_name_actual] = signal_values
        return signal_data

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
class BriefDescriptionModel:
    briefdescription: str | None = None
    """description of the method or member"""

    @property
    def text_brief_description(self) -> str:
        """
        Get the plain text (removes html markup) from the brief description field
        :return:
        """
        if self.briefdescription:
            return re.sub(r"<.*?>", "", self.briefdescription)
        else:
            return None

    @property
    def node_brief_description(self) -> et.Element:
        """
        Get the brief description html and creates a node from it
        :return: The node with the briefdescription markup as the text
        """
        if self.briefdescription:
            return et.fromstring(f"<briefdescription>{self.briefdescription}</briefdescription>")
        else:
            return None


@dataclass()
class DetailedDescriptionModel:
    """
    Model to hold description information, with convenience properties to get the content as an element
    or as plain text without html markup
    """
    detaileddescription: str = None
    """detailed description of the method or member"""

    @property
    def text_detailed_description(self) -> str:
        """
        Get the plain text (removes html markup) from the detaileddescription field
        :return:
        """
        if self.detaileddescription:
            return re.sub(r"<.*?>", "", self.detaileddescription)
        else:
            return None

    @property
    def node_detailed_description(self) -> et.Element:
        """
        Get the detailed description html and creates a node from it
        :return: The node with the detailed description markup as the text
        """
        if self.detaileddescription:
            return et.fromstring(f"<detaileddescription>{self.detaileddescription}</detaileddescription>")
        else:
            return None


@dataclass()
class EnumValueAttributes:
    """
    Data model for enumvalue tag attributes
    """
    id: str
    """A unique, auto-generated Doxygen identifier string used for cross-referencing throughout the XML structure"""
    prot: str
    """The access protection/visibility level in the source code. Possible values: public, protected, private, """

    @classmethod
    def from_xml_element(cls, member_element: et.Element) -> "EnumValueAttributes":
        attrs = member_element.attrib
        kwargs = {"id": attrs["id"], "prot": attrs["prot"]}
        return cls(**kwargs)


@dataclass(slots=True, kw_only=True)
class EnumValueModel(BriefDescriptionModel,DetailedDescriptionModel):
    """
    Data model for enumvalue tag elements
    """
    attributes: MemberDefinitionAttributes
    """Attributes for the tag"""
    name: str
    """simple name portion of the method or member name"""
    initializer: str | None = None
    """for constants and enumerators this indicates the initial value """
    enum: str | None = None
    """Used to store parent enumerator name, not part of doxygen xsd"""

    @property
    def initializer_value(self) -> str:
        return self.initializer.split(" ")[1].strip()


@dataclass(slots=True)
class MemberDefinitionAttributes:
    """
    Data model for Doxygen memberdef element attributes.
    """
    id: str
    """A unique, auto-generated Doxygen identifier string used for cross-referencing throughout the XML structure"""
    kind: str
    """Specifies the type of member. Common values include: function, variable, typedef, enum, enumvalue, 
    property, or event"""
    prot: str
    """The access protection/visibility level in the source code. Possible values: public, protected, private, 
    or package"""
    static: str
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
    strong: str | None = None
    """Used primarily for scoping controls, such as C++ scoped enums (enum class) or C# strongly-typed data structures"""
    extern: str | None = None
    """(Optional): Indicates if the variable or function is declared extern"""
    refqual: str | None = None
    """ Identifies reference equality behavior, typically used when parsing managed languages like C# or CLI."""
    noexcept: str | None = None
    """Tracks whether a function or method is declared noexcept or has a non-throwing exception specification"""
    noexceptexpression: str | None = None
    """ It captures the raw code snippet or conditional boolean logic passed inside a conditional noexcept(...) specifier"""
    nodiscard: str | None = None
    """ Tracks the standard attribute [[nodiscard]] (found in C++17 and C23)"""
    constexpr: str | None = None
    """Tracks if a function or variable is declared with the C++ constexpr specifier"""
    consteval: str | None = None
    """Tracks the C++20 consteval keyword"""
    constinit: str | None = None
    """Tracks the C++20 constinit keyword"""
    settable: str | None = None
    """C++/CLI and C# property"""
    privatesettable: str | None = None
    """C++/CLI and C# property"""
    protectedsettable: str | None = None
    """C++/CLI and C# property"""
    gettable: str | None = None
    """C++/CLI and C# property"""
    privategettable: str | None = None
    """C++/CLI and C# property"""
    protectedgettable: str | None = None
    """C++/CLI and C# property"""
    final: str | None = None
    """C++/CLI function"""
    sealed: str | None = None
    """C++/CLI function"""
    new: str | None = None
    """C++/CLI function"""
    readable: str | None = None
    """Qt property"""
    writable: str | None = None
    """Qt property"""
    add: str | None = None
    """C++/CLI event"""
    remove: str | None = None
    """C++/CLI event"""
    raise_: str | None = None
    """C++/CLI event"""
    accessor: str | None = None
    """Objective-C 2.0 property accessor"""
    initonly: str | None = None
    """C++/CLI variable"""


    @classmethod
    def from_xml_element(cls, member_element: et.Element) -> "MemberDefinitionAttributes":
        attrs = member_element.attrib
        # id is always present
        kwargs = {"id": attrs["id"]}
        # Map everything else dynamically if it exists in the XML
        for xml_key, value in attrs.items():
            if xml_key == "id":
                continue
            # Handle Python keyword conflict safely
            if xml_key == "raise":
                kwargs["raise_"] = value
            else:
                kwargs[xml_key] = value

        return cls(**kwargs)


@dataclass(slots=True)
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


@dataclass(slots=True, kw_only=True)
class MemberDefinitionModel(BriefDescriptionModel,DetailedDescriptionModel):
    """
    Used to model data from the Doxygen XML Memberdef elements
    todo: add missing elements, already have more than needed might as well complete it
      <xsd:element name="templateparamlist" type="templateparamlistType" minOccurs="0" />
      <xsd:element name="reimplements" type="reimplementType" minOccurs="0" maxOccurs="unbounded" />
      <xsd:element name="reimplementedby" type="reimplementType" minOccurs="0" maxOccurs="unbounded" />
      <xsd:element name="param" type="paramType" minOccurs="0" maxOccurs="unbounded" />
      <xsd:element name="requiresclause" type="linkedTextType" minOccurs="0" />
      <xsd:element name="exceptions" type="linkedTextType" minOccurs="0" />
      <xsd:element name="references" type="referenceType" minOccurs="0" maxOccurs="unbounded" />
      <xsd:element name="referencedby" type="referenceType" minOccurs="0" maxOccurs="unbounded" />
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
    # briefdescription: str | None = None
    """brief description of the method or member"""
    # detaileddescription: str | None = None
    """detailed description of the method or member"""
    initializer: str | None = None
    """for constants and enumerators this indicates the initial value """
    argsstring: str | None = None
    """If applicable contains the argument string for the member"""
    inbodydescription: str | None = None
    location: MemberDefinitionLocation | None = None
    read: str | None = None
    write: str | None = None
    bitfield: str | None = None
    qualifier: str | None = None
    enum_values: List[EnumValueModel] = field(default_factory=list)
    parameters: List[ParameterTypeModel] = field(default_factory=list)

    @property
    def initializer_value(self) -> str:
        if self.initializer is not None:
            return self.initializer.split(" ")[1].strip()
        else:
            return None

    @classmethod
    def from_dict(cls, data: dict):
        valid_fields = {f.name for f in fields(cls)}
        # 2. Filter the input dictionary to keep only valid fields
        filtered_data = {key: value for key, value in data.items() if key in valid_fields}
        # 3. Unpack the filtered dictionary into the class constructor
        return cls(**filtered_data)

@dataclass(slots=True,kw_only=True)
class ParameterTypeModel(BriefDescriptionModel):
    """
    Used to model data from the Doxygen XML ParameterType elements
    because it inherits DescriptionModel it will have a detailed and brief description field,
    however only the brief is ever used in a parameter type.
    """
    attributes: str | None = None
    type: str | None = None
    declname: str | None = None
    defname: str | None = None
    array: str | None = None
    defval: str | None = None
    typeconstraint: str | None = None

@dataclass(slots=True,kw_only=True)
class SimpleSectionModel:
    kind: str
    title: str | None = None
    content: str | None = None

    @property
    def node_content(self) -> et.Element:
        if self.content is not None:
            return et.fromstring(f'<content>{self.content}</content>')
        else:
            return None

    @classmethod
    def from_xml(cls, element: et.Element) -> SimpleSectionModel:
        kind = element.attrib["kind"]
        if element.find("title") is not None:
            title = element.find("title").text
        else:
            title = None
        content = get_inner_markup(element)
        return SimpleSectionModel(kind=kind, title=title, content=content)

@dataclass(slots=True,kw_only=True)
class XRefSectionModel:
    id: str
    xreftitle: str
    xrefdescription: str | None = None

    @property
    def text_description(self) -> str:
        """
        Get the plain text (removes html markup) from the detaileddescription field
        :return:
        """
        if self.xrefdescription:
            return re.sub(r"<.*?>", "", self.xrefdescription)
        else:
            return None

    @property
    def node_description(self) -> et.Element:
        """
        Get the detailed description html and creates a node from it
        :return: The node with the detailed description markup as the text
        """
        if self.xrefdescription:
            return et.fromstring(f"<xrefdescription>{self.xrefdescription}</xrefdescription>")
        else:
            return None

    @classmethod
    def from_xml(cls,xref_element:et.Element)->"XRefSectionModel":
        id = xref_element.attrib["id"]
        title_node = xref_element.find("xreftitle")
        description_node = xref_element.find("xrefdescription")
        if description_node is not None:
            description = get_inner_markup(description_node)
        else:
            description = None
        return cls(id=id, xreftitle=title_node.text, xrefdescription=description)




