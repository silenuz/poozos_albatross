#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 6/19/26
@File: eurus

@Author: Silenuz Nowan (silenuznowan@yahoo.com)

"Say 'hello' to my little friend!"
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, TypeVar

from . import luckys_zephyr
from .argestes import ClassDocModel, ClassDocConstant, ClassDocMethod, ClassDocMember, ClassDocSignal, \
    ClassDocParameter, ClassDocReturn, Description, DocConstants, DocMethods, DocMembers, DocSignals, DocParameters
from .argestes.class_doc import ExtensionDocModel # todo: add this to init imports for package
from .luckys_zephyr import LuckyZephyr, EnumValueModel, XRefSectionModel
from .poozos_notus import PoozoNotus, PropertyInfoModel
from .rossetta import Rosetta
from .boreas_rosetta import DoxygenOutputTypes


class Eurus:
    # used to convert the doxygen xml text content to bbcode
    rosetta: Rosetta

    # track methods that are getters and setters as they should be part of the members output
    # and not the methods output
    property_methods_set = set()

    def load_doxy_all(self, xml_directory: Path) -> ExtensionDocModel:
        result = ExtensionDocModel()
        files = list(xml_directory.rglob('class*.xml'))
        for file in files:
            model = self.load_doxy(file)
            result.class_docs.append(model)
        return result

    def load_doxy(self, class_xml: Path) -> ClassDocModel:
        lz = LuckyZephyr(class_xml)
        bind_methods_definition = lz.get_definition_by_tag('name', "_bind_methods")
        if bind_methods_definition is None:
            raise LookupError('Bind Methods not defined')
        else:
            code_file = next(self.source_directory.rglob(bind_methods_definition.location.bodyfile), None)
            if code_file is None:
                raise FileNotFoundError(f'Unable to locate the code file for _bind_methods, '
                                        f'filename {bind_methods_definition.location.bodyfile}')
            else:
                poozo = PoozoNotus(code_file)
                return self.__doxy_map_class(lz=lz,poozo=poozo)


    def __init__(self, source_directory: Path):
        """
        Create a Eurus instance from the Path to the Gdextension top level directory
        :param source_directory:  The Path to the top level of the GDExtension directory.
        """
        self.source_directory = source_directory
        """The Path to the top level directory of the GDExtension"""
        self.rosetta = Rosetta()
        """The Rosetta instance used to convert doxygen XML to BBCode"""

    ################################################################################################
    ###                       Doxygen + Source code to model                                     ###
    ################################################################################################

    def __doxy_map_class(self,lz:LuckyZephyr,poozo:PoozoNotus)->ClassDocModel:
        self.property_methods_set.clear()
        description = lz.get_class_detail()
        brief = lz.get_class_brief()
        description_bbcode = self.rosetta.doxygen_rosetta.doxygen_to_bbcode(description)
        brief_bbcode = self.rosetta.doxygen_rosetta.doxygen_to_bbcode(brief)
        # Note a string passed as brief or detailed description to init should work.  On post init the model will convert
        # the string to the appropriate description object
        class_model = ClassDocModel(brief_description=brief_bbcode, description=description_bbcode, name=lz.class_name)
        self.__doxy_map_properties(class_model=class_model,lz=lz,poozo=poozo)
        self.__doxy_map_methods(class_model=class_model,lz=lz,poozo=poozo)
        self.__doxy_map_integer_constants(class_model=class_model,lz=lz,poozo=poozo)
        self.__doxy_map_enums(class_model=class_model,lz=lz,poozo=poozo)
        self.__doxy_map_signals(class_model=class_model,lz=lz,poozo=poozo)
        return class_model

    def __doxy_map_enums(self, class_model:ClassDocModel,lz:LuckyZephyr,poozo:PoozoNotus)->None:
        enum_value_names = poozo.get_bound_enums()
        if len(enum_value_names) <= 0:
            return
        enum_values_doxy = lz.get_enumerator_data(enum_value_names)
        ## map by enumerator
        enum_map: dict[str, list[EnumValueModel]] = {}
        for enum_value_model in enum_values_doxy:
            if not enum_value_model.enum in enum_map:
                enum_map[enum_value_model.enum] = []
            enum_map[enum_value_model.enum].append(enum_value_model)
        if class_model.constants is None:
            class_model.constants = DocConstants()
        for enumerator in enum_map:
            enumerator_values = enum_map[enumerator]
            index = 0
            for enumerator_value in enumerator_values:
                constant = ClassDocConstant(enumerator_value.name)
                constant.enum = enumerator
                if enumerator_value.initializer_value is not None:
                    initial_value = enumerator_value.initializer_value
                    index = int(initial_value)
                constant.value = str(index)
                if enumerator_value.detaileddescription is not None:
                    constant.text = self.rosetta.doxygen_rosetta.doxygen_to_bbcode(enumerator_value.detaileddescription)
                class_model.constants.append(constant)
                index += 1

    def __doxy_map_integer_constants(self,class_model:ClassDocModel,lz:LuckyZephyr,poozo:PoozoNotus):
        bound_constants = poozo.get_bound_constants(lz.class_name)
        if len(bound_constants) <= 0:
            return
        if class_model.constants is None:
            class_model.constants = DocConstants()
        for bound_constant in bound_constants:
            member_definition = lz.get_definition_by_name(bound_constant.p_value)
            # godot docs need a value attribute for the constant
            if member_definition is not None and member_definition.initializer_value is not None:
                constant = ClassDocConstant(name=bound_constant.p_name)
                if bound_constant.p_enum:
                    constant.enum = bound_constant.p_enum
                constant.value = member_definition.initializer_value
                constant.text = self.rosetta.doxygen_rosetta.doxygen_to_bbcode(member_definition.detaileddescription)
                class_model.constants.append(constant)


    def __doxy_map_methods(self,class_model:ClassDocModel,lz:LuckyZephyr,poozo:PoozoNotus):
        # todo: test method parameters to method output
        bound_methods = poozo.get_bound_methods()
        if len(bound_methods) <= 0:
            return
        methods: DocMethods = DocMethods()
        for bound_method in bound_methods:
            if bound_method.name not in self.property_methods_set:
                member_definition = lz.get_definition_by_qualified(bound_method.qualified_method_name)
                method = ClassDocMethod(name=bound_method.name)
                if member_definition is not None:
                    method.return_value = ClassDocReturn(type_value=member_definition.type)
                    description = self.rosetta.doxygen_rosetta.doxygen_to_bbcode(member_definition.node_detailed_description)
                    method.description = Description(text=description)
                    if member_definition.parameters is not None:
                        method.parameters = DocParameters()
                        index = 0
                        for parameter in member_definition.parameters:
                            method.parameters.new(name=bound_method.args[index],type_value=parameter.type,index=str(index))
                            index += 1
                    methods.append(method)
        class_model.methods = methods

    def __doxy_map_properties(self,class_model:ClassDocModel,lz:LuckyZephyr,poozo:PoozoNotus):
        bound_properties = poozo.get_bound_properties()
        if len(bound_properties) <= 0:
            return
        members: DocMembers = DocMembers()
        for bound_property in bound_properties:
            member_definition = lz.get_definition_by_name(bound_property.field)
            member = ClassDocMember(member_definition.name)
            if member_definition.detaileddescription is not None:
                member.text = self.rosetta.doxygen_rosetta.doxygen_to_bbcode(member_definition.detaileddescription)
            member.getter = bound_property.getter
            member.setter = bound_property.setter
            assign_value(bound_property.info,member_definition.type,member)
            self.property_methods_set.add(bound_property.getter)
            self.property_methods_set.add(bound_property.setter)
            members.append(member)

        class_model.members = members

    def __doxy_map_signals(self,class_model:ClassDocModel,lz:LuckyZephyr,poozo:PoozoNotus):
        bound_signals = poozo.get_bound_signals()
        if len(bound_signals) <= 0:
            return
        signal_data: dict[str, SignalXRefDataModel] = {}
        signals_ref = lz.get_xref_items('Signal')
        for signal_ref in signals_ref:
            data = SignalXRefDataModel.from_reference_item(signal_ref)
            signal_data[data.name] = data

        signals: DocSignals = DocSignals()
        for bound_signal in bound_signals:
            signal = ClassDocSignal(bound_signal.name)
            data = signal_data[bound_signal.name]
            signal_parameters = bound_signal.argument_info
            if len(signal_parameters) > 0:
                signal.parameters = DocParameters()
                for signal_parameter_info in signal_parameters:
                    parameter = ClassDocParameter(signal_parameter_info.name)
                    parameter.index = str(signal_parameter_info.index)
                    parameter.name = signal_parameter_info.name
                    parameter.type_value = signal_parameter_info.variant_type_name
                    specified_type = signal_parameter_info.get_hint_type()
                    if specified_type is not None:
                        assign_value(signal_parameter_info,signal_parameter_info.class_name,parameter)
                    signal.parameters.append(parameter)
            if data is not None:
                description_parts = []
                description = self.rosetta.doxygen_rosetta.doxygen_to_bbcode(data.description)
                description_parts.append(description)
                headlines = lz.get_headlines_for_xrefitem(data.reference_item)
                bbcode_format_map = self.rosetta.doxygen_rosetta.output_markup_map[DoxygenOutputTypes.BBCode]
                for headline in headlines:
                    if headline.kind == 'warning' and headline.content is not None:
                        warning = self.rosetta.doxygen_rosetta.parse_xml_text(headline.node_content, bbcode_format_map)
                        description_parts.append('[br][br][b]Warning:[/b]' + ' ' + warning)
                    elif headline.kind == 'note':
                        note = self.rosetta.doxygen_rosetta.parse_xml_text(headline.node_content, bbcode_format_map)
                        description_parts.append('[br][br][b]Note:[/b]' + ' ' + note)
                signal.description = Description("".join(description_parts))
            signals.append(signal)
            if len(signals) >0:
                class_model.signals = signals


#########################################################################################################
##                    generic class to assign value from PropertyInfoModel to any object with type_value #
##                     and enum fields                                                         ##########
#############################################################################################################
class HasValueField(Protocol):
    type_value: str
    enum: str

T = TypeVar("T", bound=HasValueField)

# Your single assignment method
def assign_value(input_data: PropertyInfoModel,member_type:str, target_obj: T) -> T:
    hint_type = input_data.get_hint_type()
    if hint_type is not None:
        if hint_type[0] == 'type':
            target_obj.type_value = hint_type[1]
        elif hint_type[0] == 'enum':
            if hint_type[1] is not None:
                target_obj.enum = hint_type[1]
            else:
                target_obj.enum = member_type
    return target_obj



###################################################################################
####  Signal Model                                                             ###
###################################################################################
@dataclass(slots=True, kw_only=True)
class SignalXRefDataModel:
    name: str
    reference_item: XRefSectionModel

    @property
    def description(self) -> str:
        paragraph_block = self.reference_item.node_description.find('.//parblock')
        paragraphs = paragraph_block.findall('para')
        description_parts = []
        for paragraph in paragraphs[1:]:
            para = luckys_zephyr.get_inner_markup(paragraph)
            if para:
                description_parts.append('<para>' + para + '</para>')

        description = ".".join(description_parts)
        if description:
            return description
        else:
            return None


    @classmethod
    def from_reference_item(cls, xrefitem: XRefSectionModel) -> "SignalXRefDataModel":
        paragraph_block = xrefitem.node_description.find('.//parblock')
        paragraphs = paragraph_block.findall('para')
        name_node = paragraphs[0]
        name = "".join(name_node.itertext())
        signal_name = re.sub(r"\(.*?\):", "", name)
        return cls(name=signal_name, reference_item=xrefitem)