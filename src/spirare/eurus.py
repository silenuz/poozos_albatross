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


class Eurus:
    lz: LuckyZephyr = None
    poozo: PoozoNotus = None
    class_model: ClassDocModel = None
    rosetta: Rosetta

    # track methods that are getters and setters as they should be part of the members output
    # and not the methods output
    property_methods_set = set()

    def load_doxy_all_xml(self, source_directory: Path) -> ExtensionDocModel:
        result = ExtensionDocModel()
        files = list(source_directory.rglob('class*.xml'))
        for file in files:
            model = self.load_doxy_class_xml(file)
            result.class_doc.append(model)
        return result

    def load_doxy_class_xml(self, class_xml: Path) -> ClassDocModel:
        self.lz = LuckyZephyr(class_xml)
        bind_methods_definition = self.lz.get_definition_by_tag('name', "_bind_methods")
        if bind_methods_definition is None:
            raise LookupError('Bind Methods not defined')
        else:
            code_file = next(self.source_directory.rglob(bind_methods_definition.location.bodyfile), None)
            if code_file is None:
                raise FileNotFoundError(f'Unable to locate the code file for _bind_methods, '
                                        f'filename {bind_methods_definition.location.bodyfile}')
            else:
                self.poozo = PoozoNotus(code_file)
                self.__doxy_map_class()
                return self.class_model

    def __init__(self, source_directory: Path):
        self.source_directory = source_directory
        self.rosetta = Rosetta()

    ################################################################################################
    ###                       Doxygen + Source code to model                                     ###
    ################################################################################################

    def __doxy_map_class(self):
        self.property_methods_set.clear()
        description = self.lz.get_class_detail()
        brief = self.lz.get_class_brief()
        description_bbcode = self.rosetta.doxygen_rosetta.doxygen_to_bbcode(description)
        brief_bbcode = self.rosetta.doxygen_rosetta.doxygen_to_bbcode(brief)
        # Note a string passed as brief or detailed description to init should work.  On post init the model will convert
        # the string to the appropriate description object
        self.class_model = ClassDocModel(brief_description=brief_bbcode, description=description_bbcode, name=self.lz.class_name)
        self.__doxy_map_properties()
        self.__doxy_map_methods()
        self.__doxy_map_integer_constants()
        self.__doxy_map_enums()
        self.__doxy_map_signals()

    def __doxy_map_enums(self):
        enum_value_names = self.poozo.get_bound_enums()
        enum_values_doxy = self.lz.get_enumerator_data(enum_value_names)
        ## map by enumerator
        enum_map: dict[str, list[EnumValueModel]] = {}
        for enum_value_model in enum_values_doxy:
            if not enum_value_model.enum in enum_map:
                enum_map[enum_value_model.enum] = []
            enum_map[enum_value_model.enum].append(enum_value_model)

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
                self.class_model.constants.append(constant)
                index += 1

    def __doxy_map_integer_constants(self):
        bound_constants = self.poozo.get_bound_constants(self.lz.class_name)
        constants: DocConstants = DocConstants()
        for bound_constant in bound_constants:
            member_definition = self.lz.get_definition_by_name(bound_constant.p_value)
            # godot docs need a value attribute for the constant
            if member_definition is not None and member_definition.initializer_value is not None:
                constant = ClassDocConstant(name=bound_constant.p_name)
                if bound_constant.p_enum:
                    constant.enum = bound_constant.p_enum
                constant.value = member_definition.initializer_value
                constant.text = self.rosetta.doxygen_rosetta.doxygen_to_bbcode(member_definition.detaileddescription)
                constants.append(constant)
        self.class_model.constants = constants

    def __doxy_map_methods(self):
        bound_methods = self.poozo.get_bound_methods()
        methods: DocMethods = DocMethods()
        for bound_method in bound_methods:
            if bound_method.name not in self.property_methods_set:
                member_definition = self.lz.get_definition_by_qualified(bound_method.qualified_method_name)
                method = ClassDocMethod(name=bound_method.name)
                if member_definition is not None:
                    method.return_value = ClassDocReturn(type_value=member_definition.type)
                    description = self.rosetta.doxygen_rosetta.doxygen_to_bbcode(member_definition.detaileddescription)
                    method.description = Description(text=description)
                    methods.append(method)
        self.class_model.methods = methods

    def __doxy_map_properties(self):
        bound_properties = self.poozo.get_bound_properties()
        members: DocMembers = DocMembers()
        for bound_property in bound_properties:
            member_definition = self.lz.get_definition_by_name(bound_property.field)
            member = ClassDocMember(member_definition.name)
            if member_definition.detaileddescription is not None:
                member.text = self.rosetta.doxygen_rosetta.doxygen_to_bbcode(member_definition.detaileddescription)
            member.getter = bound_property.getter
            member.setter = bound_property.setter
            assign_value(bound_property.info,member_definition.type,member)
            self.property_methods_set.add(bound_property.getter)
            self.property_methods_set.add(bound_property.setter)
            members.append(member)

        self.class_model.members = members

    def __doxy_map_signals(self):
        bound_signals = self.poozo.get_bound_signals()
        if len(bound_signals) < 0:
            return
        signal_data: dict[str, SignalXRefDataModel] = {}
        signals_ref = self.lz.get_xref_items('Signal')
        for signal_ref in signals_ref:
            data = SignalXRefDataModel.from_reference_item(signal_ref)
            signal_data[data.name] = data

        signals: DocSignals = DocSignals()
        for bound_signal in bound_signals:
            signal = ClassDocSignal(bound_signal.name)
            data = signal_data[bound_signal.name]
            signal.description = Description(self.rosetta.doxygen_rosetta.doxygen_to_bbcode(data.description))
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
            signals.append(signal)
            if len(signals) >0:
                self.class_model.signals = signals


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