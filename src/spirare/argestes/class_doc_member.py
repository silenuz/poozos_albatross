#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 6/22/26
@File: ClassDocMember

@Author: Silenuz Nowan (silenuznowan@yahoo.com)
"""
import xml
from xml.etree.ElementTree import Element
from xml.etree import ElementTree as Et

from .doc_base import ConstantMemberBase, ModelCollection
from .zucaritas import Zucaritas


class ClassDocMember(ConstantMemberBase,Zucaritas):
    """
    This class represents a model of the class doc's member element
        
    :param str enum: The value of the enum attribute for the member element.
    :param bool is_bitfield: The value of the is_bitfield attribute for the member element.
    :param str name: The value of the name attribute for the member element.
    :param str text: The text value of the member element.
    :param bool is_deprecated: The value of the is_deprecated attribute for the member element.
    :param bool is_experimental: The value of the is_experimental attribute for the member element.
    :param str deprecated: The value of the deprecated attribute for the member element.
    :param str experimental: The value of the experimental attribute for the member element.
    :param str keywords: The value of the keywords attribute for the member element.
    :param str type_value: The value of the type attribute for the member element.
    :param str getter: The value of the getter attribute for the member element.
    :param str setter: The value of the setter attribute for the member element.
    :param str overrides: The value of the overrides attribute for the member element.
    :param str default: The value of the default attribute for the member element.

    "Open the pod bay doors, please, HAL"
    """
    __slots__ = ('type_value','getter','setter','overrides','default')
    type_value: str
    """The value of the type attribute for the member element"""
    getter: str
    """The value of the getter attribute for the member element"""
    setter: str
    """The value of the setter attribute for the member element"""
    overrides: str
    """The value of the overrides attribute for the member element"""
    default: str
    """The value of the default attribute for the member element"""


    def __init__(self, name: str, type_value: str = None,getter:str=None,setter:str = None,text: str = None,
                 overrides:str=None, default:str=None,enum: str = None, is_bitfield: bool = None,
                 keywords: str = None, is_deprecated: bool = None, is_experimental: bool = None,
                 deprecated: str = None, experimental: str = None):
        super().__init__(name=name, text=text, enum=enum, is_bitfield=is_bitfield, keywords=keywords,
                         is_deprecated=is_deprecated, is_experimental=is_experimental, deprecated=deprecated,
                         experimental=experimental)
        self.type_value = type_value
        """The value of the type attribute for the member element"""
        self.getter = getter
        """The value of the getter attribute for the member element"""
        self.setter = setter
        """The value of the setter attribute for the member element"""
        self.overrides = overrides
        """The value of the overrides attribute for the member element"""
        self.default = default
        """The value of the default attribute for the member element"""

    def to_dict(self) -> dict:
        """
       Returns a dictionary of the values for this member element model instance.

       :return: a dictionary of values for this member model instance.
       """
        values = dict()
        if self.type_value is not None:
            values['type_value'] = self.type_value
        if self.getter is not None:
            values['getter'] = self.getter
        if self.setter is not None:
            values['setter'] = self.setter
        if self.overrides is not None:
            values['overrides'] = self.overrides
        if self.default is not None:
            values['default'] = self.default
        values.update(super().to_dict())
        return values

    def to_xml_doc(self)->xml.etree.ElementTree.Element:
        """
        Create a Godot class doc element for this member model instance.

        :return: A Godot class doc element for this member model instance.
        """
        base_element = self._to_xml()
        base_element.tag = 'member'
        return base_element


############################################################################################
###                         Members List Model                                           ###
###########################################################################################


class DocMembers(ModelCollection):
    """
    This class models the members element, and contains a list of ClassDocMember instances.

    :param list initlist: A list of ClassDocMember instances.

    "Careful! Combining those items might cause a rip in the space-time continuum, a tear in the very fabric of space itself! (Or not.)"
    """
    def __init__(self,initlist=None):
        super().__init__(ClassDocMember, initlist)

    def new(self, **kwargs) -> ClassDocMember:
        """
        Creates a new ClassDocMember instance and adds it to the list.

        :param kwargs: Keyword arguments for the new ClassDocMember instance.
        :return: The new ClassDocMember instance.
        """
        member = ClassDocMember(**kwargs)
        self.append(member)
        return member

    def to_dict(self) -> dict:
        """
       Returns a dictionary of the values for this members' element model instance.

       :return: a dictionary of values for this members' model instance.
       """
        result = dict()
        result['members'] = []
        for member in self.data:
            result['members'].append(member.to_dict())
        return result


    def to_xml_doc(self)->xml.etree.ElementTree.Element:
        """
        Create a Godot class doc element for this members list instance.

        :return: A Godot class doc element for this members list instance.
        """
        element = Et.Element('members')
        for member in self.data:
          element.append(member.to_xml_doc())
        return element

    @classmethod
    def from_json(cls, json_str: str)->'DocMembers':
        """
        Create a new DocMembers instance from a JSON string.

        :param json_str: the JSON string containing the members' data.
        :return: A new DocMembers instance.
        """
        return super().from_json(ClassDocMember, json_str)

    @classmethod
    def from_xml(cls, element:xml.etree.ElementTree.Element):
        initial_list = [ClassDocMember.from_xml(e) for e in element]
        return cls(initial_list)