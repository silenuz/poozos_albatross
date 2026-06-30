#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 6/21/26
@File: doc_base

@Author: Silenuz Nowan (silenuznowan@yahoo.com)
"""
from __future__ import annotations
import json
import typing
from collections import UserList
import xml.etree.ElementTree as Et

import json


# class JsonBase:
#     @classmethod
#     def from_json(cls, json_data: str):
#         # 1. Parse the JSON string into a raw Python dictionary
#         raw_data = json.loads(json_data)
#
#         # 2. Extract top-level primitive attributes for the constructor
#         init_kwargs = {}
#         for key, value in raw_data.items():
#
#         # Create the base object instance
#         class_object = cls(**init_kwargs)
#
#         # 3. Process complex types (nested objects and custom lists) using type hints
#         for key, value in raw_data.items():
#             mapped_key = cls.attribute_map.get(key, key) if hasattr(cls, 'attribute_map') else key
#             attr_type = cls.__annotations__.get(mapped_key)
#
#             if isinstance(attr_type, str):
#                 import sys
#                 current_module = sys.modules[cls.__module__]
#                 attr_type = getattr(current_module, attr_type, None)
#
#             if attr_type is not None:
#                 # If it's a custom list class (like DocParameters) or nested object
#                 if hasattr(attr_type, 'from_json'):
#                     # If the child class has a from_json method, delegate to it
#                     child_instance = attr_type.from_json(json.dumps(value))
#                     setattr(class_object, mapped_key, child_instance)
#                 else:
#                     # Otherwise, try passing the raw list/dict straight into its constructor
#                     # (e.g., DocParameters(value))
#                     try:
#                         child_instance = attr_type(value)
#                         setattr(class_object, mapped_key, child_instance)
#                     except TypeError:
#                         pass
#
#         return class_object
#
#     def to_json(self):
#         return json.dumps(self.to_dict())


class JsonBase:
    @classmethod
    def from_json(cls, json_data):
        raw_args = json.loads(json_data)
        kwargs={}
        for key,value in raw_args.items():
            attrib_type = typing.get_type_hints(cls).get(key)
            if attrib_type is not None and hasattr(attrib_type, 'from_json'):
                kwargs[key] = attrib_type.from_json(value)
            else:
                kwargs[key] = value

        return  cls(**kwargs)

    def to_json(self):
        return json.dumps(self.to_dict())

class GodotBase:
    attribute_map = dict()
    attribute_map['type'] = 'type_value'

    def get_inner_markup(self,element: Et.Element) -> str:
        # 1. Grab the initial text chunk before any child tag
        parts = [element.text or ""]
        for child in element:
            # encoding="unicode" returns a standard python string instead of bytes
            parts.append(Et.tostring(child, encoding="unicode"))
        return "".join(parts).strip()

    @classmethod
    def from_xml(cls, element:Et.Element):
        kwargs = dict()
        for key,value in element.attrib.items():
            if not 'http' in key:
                if key in cls.attribute_map:
                    key = cls.attribute_map[key]
                kwargs[key] = value
        class_object = cls(**kwargs)
        if element.text is not None and hasattr(class_object, 'text'):
            class_object.text = class_object.get_inner_markup(element)
        for e in element:
            if e.tag == 'param':
                if class_object.parameters is None:
                    class_object.parameters = DocParameters()
                class_object.parameters.append(ClassDocParameter.from_xml(e))
            else:
                attr_type = typing.get_type_hints(class_object.__class__).get(e.tag)
                print("Element Tag:: ", e.tag)
                print("Attribute Type:: ", attr_type)
                if attr_type is not None:
                    child = attr_type.from_xml(e)
                    setattr(class_object, e.tag, child)
        return class_object

    def _to_xml(self):
        values = self.to_dict()
        element = Et.Element('element')
        for key,value in values.items():
            if key == 'text':
                element.text = value
            else:
                attr_type = typing.get_type_hints(self.__class__).get(key)
                #attr_type = self.__annotations__.get(key)
                if attr_type is not None and not getattr(attr_type, '__module__', None) == 'builtins':
                    attr_instance = getattr(self, key, None)
                    #print(attr_type)
                    if attr_type == DocParameters:
                        params = attr_instance.to_xml_doc()
                        if isinstance(params,Et.Element):
                            element.append(params)
                        else:
                            for param in params:
                                #print("append parameter")
                                element.append(param)
                    elif hasattr(attr_instance, 'to_xml_doc'):
                        #print("append element")
                        sub_element = attr_instance.to_xml_doc()
                        if sub_element is not None:
                            element.append(sub_element)
                else:
                    #print("key:: ", key)
                    element.set(key,str(value))
        return element


class DocQualifierBase:
    __slots__ = ('enum', 'is_bitfield')
    enum: str
    is_bitfield: bool

    def __init__(self, enum: str = None, is_bitfield: bool = False) -> None:
        self.enum = enum
        self.is_bitfield = is_bitfield

    def to_dict(self) -> dict:
        values = dict()
        if self.enum is not None:
            values['enum'] = self.enum
        if self.is_bitfield is not None:
            values['is_bitfield'] = self.is_bitfield
        return values


class DescriptionBase:
    __slots__ = ('text','_element_name')
    text: str
    _element_name: str

    def __init__(self, text: str = '') -> None:
        self.text = text

    def __post_init__(self) -> None:
        if self.text is None:
            self.text = ''

    def to_dict(self) -> dict:
        return {self._element_name: self.text}

    def to_xml_doc(self):
        if self.text:
            element = Et.Element(self._element_name)
            element.text = self.text
            return element
        return None

    @classmethod
    def from_xml(cls,element: Et.Element):
        return cls(text=element.text)

    @classmethod
    def from_json(cls,json_data: str):
        return cls(text=json_data)


class DocBriefDescription(DescriptionBase):
    __slots__ = ()

    def __init__(self, text: str = ''):
        super().__init__(text)
        self._element_name = 'brief_description'


class DocDescription(DescriptionBase):
    __slots__ = ()

    def __init__(self, text: str = ''):
        super().__init__(text)
        self._element_name = 'description'


class MemberBase(DocQualifierBase):
    __slots__ = ('name', 'text')
    name: str
    text: str

    def __init__(self, name: str, text: str = None, enum: str = None,
                 is_bitfield: bool = False) -> None:
        super().__init__(enum=enum, is_bitfield=is_bitfield)
        self.name = name
        self.text = text

    def to_dict(self) -> dict:
        values = dict()
        if self.name is not None:
            values['name'] = self.name
        if self.text is not None:
            values['text'] = self.text
        values.update(super().to_dict())
        return values


class MemberBaseTags(MemberBase):
    __slots__ = ('is_deprecated', 'is_experimental', 'deprecated', 'experimental')
    is_deprecated: bool
    is_experimental: bool
    deprecated: str
    experimental: str

    def __init__(self, name: str, text: str = None, enum: str = None, is_bitfield: bool = False,
                 is_deprecated: bool = False, is_experimental: bool = False,
                 deprecated: str = None, experimental: str = None) -> None:
        super().__init__(name=name, text=text, enum=enum, is_bitfield=is_bitfield)
        self.is_deprecated = is_deprecated
        self.is_experimental = is_experimental
        self.deprecated = deprecated
        self.experimental = experimental

    def to_dict(self) -> dict:
        values = super().to_dict()
        if self.is_deprecated is not None:
            values['is_deprecated'] = self.is_deprecated
        if self.is_experimental is not None:
            values['is_experimental'] = self.is_experimental
        if self.deprecated is not None:
            values['deprecated'] = self.deprecated
        if self.experimental is not None:
            values['experimental'] = self.experimental
        return values


class ConstantMemberBase(MemberBaseTags):
    __slots__ = 'keywords'
    keywords: str

    def __init__(self, name: str, text: str = None, enum: str = None, is_bitfield: bool = False,
                 keywords: str = None, is_deprecated: bool = False, is_experimental: bool = False,
                 deprecated: str = None, experimental: str = None) -> None:
        super().__init__(name=name, text=text, enum=enum, is_bitfield=is_bitfield,
                         is_deprecated=is_deprecated, is_experimental=is_experimental, deprecated=deprecated,
                         experimental=experimental)
        self.keywords = keywords

    def to_dict(self) -> dict:
        values = super().to_dict()
        if self.keywords is not None:
            values['keywords'] = self.keywords
        return values


class MethodBase:
    __slots__ = ('name', 'description', 'qualifiers','parameters')
    name: str
    description: DocDescription
    qualifiers: str
    parameters: DocParameters

    def __init__(self, name: str, description: DocDescription = None, qualifiers:str = None, parameters: DocParameters = None) -> None:
        self.name = name
        self.description = description
        self.qualifiers = qualifiers
        self.parameters = parameters

    # def __post_init__(self):
    #     if isinstance(self.description,str):
    #         self.description = DocDescription(text=self.description)


    def to_dict(self) -> dict:
        result = dict()
        if self.name is not None:
            result['name'] = self.name
        if self.description is not None:
            result.update(self.description.to_dict())
        if self.qualifiers is not None:
            result['qualifiers'] = self.qualifiers
        if self.parameters is not None:
            result.update(self.parameters.to_dict())
        return result


class MethodReturnBase(MethodBase):
    __slots__ = 'return_value'
    return_value: ClassDocReturn

    def __init__(self, name: str, description: DocDescription=None,qualifiers:str = None,
                 parameters: DocParameters = None, return_value: ClassDocReturn = None) -> None:
        super().__init__(name=name, description=description, qualifiers=qualifiers,parameters=parameters)
        self.return_value = return_value

    def to_dict(self) -> dict:
        values = dict()
        if self.return_value is not None:
            values['return_value'] = self.return_value.to_dict()
        values.update(super().to_dict())
        return values

class ModelCollection(UserList):
    """A generic, reusable list that enforces types.  DO NOT USE DIRECTLY
    if your expecting from_json to work as it's meant to return a subclass
    of this class"""

    def __init__(self, model_cls, initlist=None):
        self.model_cls = model_cls  # Dynamically remember what type of object this list holds
        super().__init__(initlist)
        #if initlist is not None:
            #self.extend(initlist)

    # Intercept mutations to enforce the correct model type
    def append(self, item):
        self._validate(item)
        super().append(item)

    def insert(self, i, item):
        self._validate(item)
        super().insert(i, item)

    def __setitem__(self, i, item):
        self._validate(item)
        super().__setitem__(i, item)

    def _validate(self, item):
        if not isinstance(item, self.model_cls):
            raise TypeError(f"Only {self.model_cls.__name__} objects are allowed.")

    def to_json(self) -> str:
        return json.dumps([item.to_dict() for item in self.data])

    @classmethod
    def from_json(cls, model_cls, json_str: str):
        data_list = json_str# json.loads(json_str)
        # return cls(model_cls, [model_cls.from_dict(d) for d in data_list])
        initial_list =  [model_cls.from_json(json.dumps(d)) for d in data_list]
        return cls(initial_list)



#########################################################################################################################
###                                              Doc Classes                                                          ###
#########################################################################################################################


class ClassDocReturn(DocQualifierBase,JsonBase,GodotBase):
    """
    This class represents a model of the method return element of the class docs
    Note: type_value is used as the attribute here because type is a soft keyword in python.

    :param str enum: The value of the enum attribute for return element.
    :param bool is_bitfield: The value of the is_bitfield attribute for return element.
    :param str type_value: The value of the type attribute for return element.
    """
    __slots__ = 'type_value'
    type_value: str
    """The value of the type attribute for return element."""

    def __init__(self, type_value: str = None, enum: str = None, is_bitfield: bool = False) -> None:
        super().__init__(enum, is_bitfield)
        self.type_value = type_value

    def to_dict(self) -> dict:
        result = dict()
        if self.type_value is not None:
            result['type_value'] = self.type_value
        result.update(super().to_dict())
        return result

    def to_xml_doc(self)->Et.Element:
        base_element = self._to_xml()
        base_element.tag = 'return'
        return base_element



class ClassDocParameter(ClassDocReturn,JsonBase,GodotBase):
    """
    This class represents a model of the class doc's parameter element, used in signals, methods, etc...
    
    :param str enum: The value of the enum attribute for the parameter element.
    :param bool is_bitfield: The value of the is_bitfield attribute for the parameter element.
    :param str type_value: The value of the type_value attribute for the parameter element.
    :param str index: The value of the index attribute for the parameter element.
    :param str name: The value of the name attribute for the parameter element.
    :param str default: The value of the default attribute for the parameter element.
    """
    __slots__ = ('index', 'name', 'default')
    index: str
    """The value of the index attribute for the parameter element."""
    name: str
    """The value of the name attribute for the parameter element."""
    default: str
    """ The value of the default attribute for the parameter element."""

    def __init__(self, name: str, index: str = None, default: str = None, type_value: str = None, enum: str = None,
        is_bitfield: bool = None) -> None:
        super().__init__(type_value=type_value, enum=enum, is_bitfield=is_bitfield)
        self.name = name
        self.index = index
        self.default = default

    def to_dict(self) -> dict:
        result = dict()
        if self.name is not None:
            result['name'] = self.name
        if self.default is not None:
            result['default'] = self.default
        if self.index is not None:
            result['index'] = self.index
        result.update(super().to_dict())
        return result

    def to_xml_doc(self)->Et.Element:
        base_element = self._to_xml()
        base_element.tag = 'param'
        return base_element

class ClassDocReturnError(JsonBase,GodotBase):
    """
    This class represents a model of the return error element of the class docs

    :param int number: The value of the number attribute for this element.
    """
    __slots__ = 'number'
    number: int
    """The value of the number attribute for this element"""

    def __init__(self, number: int) -> None:
        self.number = number

    def to_dict(self) -> dict:
        result = dict()
        result['number'] = self.number


    def to_xml_doc(self)->Et.Element:
        base_element = self._to_xml()
        base_element.tag = 'returns_error'
        return base_element

class ClassDocTutorialLink(JsonBase, GodotBase):
    """
    This class represents a model of the class doc's tutorial link element

    :param str text: The value of the text attribute for this element, in this case a tutorial link..
    :param str title: The value of the title attribute for this element.

    """
    __slots__ = ('text','title')
    text: str
    """URL link to the tutorial"""
    title: str
    """The title of the tutorial"""

    def __init__(self, text: str=None, title: str=None) -> None:
        self.text = text
        self.title = title

    def to_dict(self) -> dict:
        result = dict()
        if self.text is not None:
            result['text'] = self.text
        if self.title is not None:
            result['title'] = self.title
        return result

    def to_xml_doc(self)->Et.Element:
        base_element = self._to_xml()
        base_element.tag = 'link'
        return base_element


class DocReturnErrorsList(ModelCollection):
    def __init__(self, initlist=None):
        super().__init__(ClassDocReturnError, initlist)

    def new(self, number: int) -> ClassDocReturnError:
        error = ClassDocReturnError(number)
        self.append(error)
        return error

    def to_dict(self) -> dict:
        result = dict()
        result['returns_error'] = []
        for error in self.data:
            result['returns_error'].append(error.to_dict())
        return result

    @classmethod
    def from_json(cls, json_str: str):
        return super().from_json(ClassDocReturnError, json_str)

    @classmethod
    def from_xml(cls, element: Et.Element):
        initial_list = [ClassDocReturnError.from_xml(e) for e in element]
        return cls(initial_list)


class DocParameters(ModelCollection):
    def __init__(self,initlist=None):
        super().__init__(ClassDocParameter, initlist)

    def new(self, **kwargs) -> ClassDocParameter:
        parameter = ClassDocParameter(**kwargs)
        self.append(parameter)
        return parameter

    def to_dict(self) -> dict:
        result = dict()
        result['parameters'] = []
        for parameter in self.data:
            result['parameters'].append(parameter.to_dict())
        return result

    def to_xml_doc(self)->list[Et.Element]:
        elements = []
        for parameter in self.data:
            elements.append(parameter.to_xml_doc())
        return elements

    @classmethod
    def from_json(cls, json_str: str):
        return super().from_json(ClassDocParameter, json_str)

    @classmethod
    def from_xml(cls, element: Et.Element):
        initial_list = [ClassDocParameter.from_xml(e) for e in element]
        return cls(initial_list)


class DocTutorials(ModelCollection):
    def __init__(self,initlist=None):
        super().__init__(ClassDocTutorialLink, initlist)

    def new(self, **kwargs) -> ClassDocTutorialLink:
        link = ClassDocTutorialLink(**kwargs)
        self.append(link)
        return link

    def to_dict(self) -> dict:
        result = dict()
        result['tutorials'] = []
        for parameter in self.data:
            result['tutorials'].append(parameter.to_dict())
        return result

    @classmethod
    def from_json(cls, json_str: str):
        return super().from_json(ClassDocTutorialLink, json_str)

    @classmethod
    def from_xml(cls, element: Et.Element):
        initial_list = [ClassDocTutorialLink.from_xml(e) for e in element]
        return cls(initial_list)