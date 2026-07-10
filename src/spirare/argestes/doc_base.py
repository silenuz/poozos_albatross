#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 6/21/26
@File: doc_base

@Author: Silenuz Nowan (silenuznowan@yahoo.com)
"""
from __future__ import annotations
import typing
from collections import UserList
import xml.etree.ElementTree as Et
import json
import xml

class Zucaritas:
    """
    Cereal base for top level objects, providing serialization and deserialization between XML and JSON,
    for Godot documentation elements.

    "Never get out of the boat!"
    """
    attribute_map = dict()
    """ map of attributes that were renamed, currently just type is renamed because it shadows a soft keyword in python"""
    attribute_map['type'] = 'type_value'

    @classmethod
    def from_json(cls, json_data):
        """
        Create a model of this element from a JSON string

        :param json_data: JSON string with element data
        :return: A model of the element created from the JSON string
        """
        raw_args = json.loads(json_data)
        kwargs = {}
        for key, value in raw_args.items():
            attrib_type = typing.get_type_hints(cls).get(key)
            if attrib_type is not None and hasattr(attrib_type, 'from_json'):
                kwargs[key] = attrib_type.from_json(value)
            else:
                kwargs[key] = value

        return cls(**kwargs)

    def to_json(self)->str:
        """
        Returns the model of this element as a JSON string

        :return: A JSON string with element data
        """
        return json.dumps(self.to_dict(), indent=4)

    def get_inner_markup(self,element: xml.etree.ElementTree.Element) -> str:
        """
        Gets the text content of an XML element  by iterating the markup and creating a single
        string

        :param element: The element with .text content to parse
        :return: a string with the text content of the element passed as an argument
        """
        # 1. Grab the initial text chunk before any child tag
        parts = [element.text or ""]
        for child in element:
            # encoding="unicode" returns a standard python string instead of bytes
            parts.append(Et.tostring(child, encoding="unicode"))
        return "".join(parts).strip()

    @classmethod
    def from_xml(cls,element: xml.etree.ElementTree.Element):
        """
        Creates this model from a Godot class documentation XML element

        :param element: The element represented by this model
        :return: A model created from the XML documentation element
        """
        kwargs = dict()
        for key, value in element.attrib.items():
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
            elif e.tag == 'returns_error':
                if class_object.returns_error is None:
                    class_object.returns_error = DocReturnErrorsList()
                class_object.returns_error.append(ClassDocReturnError.from_xml(e))
            else:
                attr_type = typing.get_type_hints(class_object.__class__).get(e.tag)
                if attr_type is not None:
                    child = attr_type.from_xml(e)
                    setattr(class_object, e.tag, child)
        return class_object

    def _to_xml(self)->xml.etree.ElementTree.Element:
        """
        Internal method used to convert this model to generic XML, so the child class can apply
        the appropriate tags in their to_xml_doc implementation.

        :return: a generic XML element named element based on the model data
        """
        values = self.to_dict()
        element = Et.Element('element')
        for key, value in values.items():
            if key == 'text':
                element.text = value
            else:
                attr_type = typing.get_type_hints(self.__class__).get(key)
                # attr_type = self.__annotations__.get(key)
                if attr_type is not None and not getattr(attr_type, '__module__', None) == 'builtins':
                    attr_instance = getattr(self, key, None)
                    # print(attr_type)
                    if attr_type == DocParameters:
                        params = attr_instance.to_xml_doc()
                        if isinstance(params, Et.Element):
                            element.append(params)
                        else:
                            for param in params:
                                # print("append parameter")
                                element.append(param)
                    elif attr_type == DocReturnErrorsList:
                        errors = attr_instance.to_xml_doc()
                        for error in errors:
                            element.append(error)
                    elif hasattr(attr_instance, 'to_xml_doc'):
                        # print("append element")
                        sub_element = attr_instance.to_xml_doc()
                        if sub_element is not None:
                            element.append(sub_element)
                else:
                    element.set(key, str(value))
        return element


class QualifierBase:
    """
    Base class for elements with enum and is_bitfield attributes

    :param str enum: enum attribute value
    :param bool is_bitfield: is_bitfield attribute value

    "Operator! Give me the number for 911!"
    """
    __slots__ = ('enum', 'is_bitfield')
    enum: str
    """The value of the enum attribute for this element"""
    is_bitfield: bool
    """The value of the is_bitfield attribute for this element"""

    def __init__(self, enum: str = None, is_bitfield: bool = False) -> None:
        self.enum = enum
        """enum attribute value"""
        self.is_bitfield = is_bitfield
        """is_bitfield attribute value"""

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of this object.

        :return: a dictionary of values for this object
        """
        values = dict()
        if self.enum is not None:
            values['enum'] = self.enum
        if self.is_bitfield is not None:
            values['is_bitfield'] = self.is_bitfield
        return values


class DescriptionBase:
    """
    Base class for description elements such as description and brief_description

    :param str text: the text value of the element

    "1. Cover for me
     2. Oh, good idea boss!
     3. It was like that when I got here."
    """
    __slots__ = ('text', '_element_name')
    text: str
    """The text value of the element"""
    _element_name: str
    """The name of the element, used by child class to set element tag"""

    def __init__(self, text: str = '') -> None:
        self.text = text
        """The text value of the element"""

    def __post_init__(self) -> None:
        if self.text is None:
            self.text = ''

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of this object.

        :return: a dictionary of values for this object
        """
        return {self._element_name: self.text}

    def to_xml_doc(self)->xml.etree.ElementTree.Element:
        """
        Return the contents of the description as a Godot documentation XML element

        :return: this description object as a Godot XML element, the tag is based on the _element_name attribute
        """
        element = Et.Element(self._element_name)
        element.text = self.text
        return element

    @classmethod
    def from_xml(cls,element: xml.etree.ElementTree.Element):
        """
        Creates a description object from a Godot XML element

        :param element: The description or brief_description element to create the model from
        :return: A new description object with the values from the Godot XML element
        """
        return cls(text=element.text)

    @classmethod
    def from_json(cls, json_data: str):
        """
        Creates a description object from a JSON string

        :param json_data: The description or brief_description JSON content to create the model from
        :return: A new description object with the values from the JSON content
        """
        return cls(text=json_data)


class BriefDescription(DescriptionBase):
    """
    Model for brief_description elements

    :param str text: the text value of the brief_description element

    “Facts are meaningless. You can use facts to prove anything that’s even remotely true.”
    """
    __slots__ = ()

    def __init__(self, text: str = ''):
        super().__init__(text)
        self._element_name = 'brief_description'


class Description(DescriptionBase):
    """
    Model for description elements

    :param str text: the text value of the description element

    "Well, excuse me for having enormous flaws I don't work on"
    """
    __slots__ = ()

    def __init__(self, text: str = ''):
        super().__init__(text)
        self._element_name = 'description'


class MemberBase(QualifierBase):
    """
    Base class extending qualifiers

    :param str enum: The value of the enum attribute for this element.
    :param bool is_bitfield: The value of the is_bitfield attribute for this element.
    :param str name: The value of the name attribute for this element.
    :param str text: The text value for this element.

    "Oh, people can come up with statistics to prove anything, Kent. 14% of people know that."
    """
    __slots__ = ('name', 'text')
    name: str
    """The value of the name attribute for this element."""
    text: str
    """The text value for this element"""

    def __init__(self, name: str, text: str = None, enum: str = None,
                 is_bitfield: bool = False) -> None:
        super().__init__(enum=enum, is_bitfield=is_bitfield)
        self.name = name
        """The value of the name attribute for this element."""
        self.text = text
        """The text value for this element"""

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of this object.

        :return: a dictionary of values for this object
        """
        values = dict()
        if self.name is not None:
            values['name'] = self.name
        if self.text is not None:
            values['text'] = self.text
        values.update(super().to_dict())
        return values


class MemberBaseTags(MemberBase):
    """
    Base class extending MemberBase

    :param str enum: The value of the enum attribute for this element.
    :param bool is_bitfield: The value of the is_bitfield attribute for this element.
    :param str name: The value of the name attribute for this element.
    :param str text: The text value for this element.
    :param bool is_deprecated: The value of the is_deprecated attribute for this element.
    :param bool is_experimental: The value of the is_experimental attribute for this element.
    :param str deprecated: The value of the deprecated attribute for this element.
    :param str experimental: The value of the experimental attribute for this element.

    "Trying is the first step towards failure"
    """
    __slots__ = ('is_deprecated', 'is_experimental', 'deprecated', 'experimental')
    is_deprecated: bool
    """The value of the is_deprecated attribute for this element"""
    is_experimental: bool
    """The value of the is_experimental attribute for this element"""
    deprecated: str
    """The value of the deprecated attribute for this element"""
    experimental: str
    """The value of the experimental attribute for this element"""

    def __init__(self, name: str, text: str = None, enum: str = None, is_bitfield: bool = False,
                 is_deprecated: bool = False, is_experimental: bool = False,
                 deprecated: str = None, experimental: str = None) -> None:
        super().__init__(name=name, text=text, enum=enum, is_bitfield=is_bitfield)
        self.is_deprecated = is_deprecated
        """The value of the is_deprecated attribute for this element"""
        self.is_experimental = is_experimental
        """The value of the is_experimental attribute for this element"""
        self.deprecated = deprecated
        """The value of the deprecated attribute for this element"""
        self.experimental = experimental
        """The value of the experimental attribute for this element"""

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of this object.

        :return: a dictionary of values for this object
        """
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
    """
    Base class extending MemberBaseTags

    :param str enum: The value of the enum attribute for this element.
    :param bool is_bitfield: The value of the is_bitfield attribute for this element.
    :param str name: The value of the name attribute for this element.
    :param str text: The value of the text attribute for this element.
    :param bool is_deprecated: The value of the is_deprecated attribute for this element.
    :param bool is_experimental: The value of the is_experimental attribute for this element.
    :param str deprecated: The value of the deprecated attribute for this element.
    :param str experimental: The value of the experimental attribute for this element.
    :param str keywords: The value of the keywords attribute for this element.

    " I think Smithers picked me because of my motivational skills.
    Everyone says they have to work a lot harder when I’m around."
    """
    __slots__ = 'keywords'
    keywords: str
    """The value of the keywords attribute for this element"""

    def __init__(self, name: str, text: str = None, enum: str = None, is_bitfield: bool = False,
                 keywords: str = None, is_deprecated: bool = False, is_experimental: bool = False,
                 deprecated: str = None, experimental: str = None) -> None:
        super().__init__(name=name, text=text, enum=enum, is_bitfield=is_bitfield,
                         is_deprecated=is_deprecated, is_experimental=is_experimental, deprecated=deprecated,
                         experimental=experimental)
        self.keywords = keywords
        """The value of the keywords attribute for this element"""

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of this object.

        :return: a dictionary of values for this object
        """
        values = super().to_dict()
        if self.keywords is not None:
            values['keywords'] = self.keywords
        return values


class MethodBase:
    """
    Base class for method and method like elements

    :param str name: The value of the name attribute for this element.
    :param Description description: The value of the description element for this element.
    :param str qualifiers: The value of the qualifiers attribute for this element.
    :param DocParameters parameters: The value of the parameters element for this element.

    "If something’s hard to do, then it’s not worth doing"
    """
    __slots__ = ('name', 'description', 'qualifiers', 'parameters')
    name: str
    """The value of the name attribute for this element"""
    description: Description
    """The value of the description element for this element"""
    qualifiers: str
    """The value of the qualifiers attribute for this element"""
    parameters: DocParameters
    """The DocParameters list representing the param elements for this element"""

    def __init__(self, name: str, description: Description = None, qualifiers: str = None,
                 parameters: DocParameters = None) -> None:
        self.name = name
        """The value of the name attribute for this element"""
        self.description = description
        """The value of the description element for this element"""
        self.qualifiers = qualifiers
        """The value of the qualifiers attribute for this element"""
        self.parameters = parameters
        """The DocParameters list representing the param elements for this element"""

    def __post_init__(self):
        if isinstance(self.description, str):
            self.description = Description(text=self.description)

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of this object.

        :return: a dictionary of values for this object
        """
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
    """
    Base class extending MethodBase with a return element

    :param str name: The value of the name attribute for this element.
    :param Description description: The value of the description element for this element.
    :param str qualifiers: The value of the qualifiers attribute for this element.
    :param DocParameters parameters: The value of the parameters element for this element.
    :param ClassDocReturn return_value: The value of the return_value element for this element.

    " ‘To Start Press Any Key’. Where’s the ANY key?"
    """
    __slots__ = 'return_value'
    return_value: ClassDocReturn
    """The value of the return_value element for this element"""

    def __init__(self, name: str, description: Description = None, qualifiers: str = None,
                 parameters: DocParameters = None, return_value: ClassDocReturn = None) -> None:
        super().__init__(name=name, description=description, qualifiers=qualifiers, parameters=parameters)
        self.return_value = return_value
        """The value of the return_value element for this element"""

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of this object.

        :return: a dictionary of values for this object
        """
        values = dict()
        if self.return_value is not None:
            values['return_value'] = self.return_value.to_dict()
        values.update(super().to_dict())
        return values


class ModelCollection(UserList):
    """
    A generic, reusable list that enforces types.  DO NOT USE DIRECTLY
    if your expecting from_json to work as it's meant to return a subclass
    of this class
    """

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
        data_list = json_str  # json.loads(json_str)
        # return cls(model_cls, [model_cls.from_dict(d) for d in data_list])
        initial_list = [model_cls.from_json(json.dumps(d)) for d in data_list]
        return cls(initial_list)


#########################################################################################################################
###                                              Doc Classes                                                          ###
#########################################################################################################################


class ClassDocReturn(QualifierBase, Zucaritas):
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
        """The value of the type attribute for return element."""

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of this object.

        :return: a dictionary of values for this object
        """
        result = dict()
        if self.type_value is not None:
            result['type_value'] = self.type_value
        result.update(super().to_dict())
        return result

    def to_xml_doc(self) -> xml.etree.ElementTree.Element:
        """
        Return the contents of the return object as a Godot documentation XML element

        :return: this return object as a Godot XML element
        """
        base_element = self._to_xml()
        base_element.tag = 'return'
        return base_element


class ClassDocParameter(ClassDocReturn, Zucaritas):
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
    name: str
    """The value of the name attribute for the parameter element."""
    index: str  ## todo: check if this is string or int
    """The value of the index attribute for the parameter element."""
    default: str
    """ The value of the default attribute for the parameter element."""

    def __init__(self, name: str, index: str = None, default: str = None, type_value: str = None, enum: str = None,
                 is_bitfield: bool = None) -> None:
        super().__init__(type_value=type_value, enum=enum, is_bitfield=is_bitfield)
        self.name = name
        """The value of the name attribute for the parameter element."""
        self.index = index
        """The value of the index attribute for the parameter element."""
        self.default = default
        """ The value of the default attribute for the parameter element."""

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of this object.

        :return: a dictionary of values for this object
        """
        result = dict()
        if self.name is not None:
            result['name'] = self.name
        if self.default is not None:
            result['default'] = self.default
        if self.index is not None:
            result['index'] = self.index
        result.update(super().to_dict())
        return result

    def to_xml_doc(self) -> xml.etree.ElementTree.Element:
        """
        Return the contents of the parameter (param) object as a Godot documentation XML element

        :return: this parameter object as a Godot XML element
        """
        base_element = self._to_xml()
        base_element.tag = 'param'
        return base_element


class ClassDocReturnError(Zucaritas):
    """
    This class represents a model of the return error element of the class docs

    :param int number: The value of the number attribute for this element.
    """
    __slots__ = 'number'
    number: int
    """The value of the number attribute for this element"""

    def __init__(self, number: int) -> None:
        self.number = number
        """The value of the number attribute for this element"""

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of this object.

        :return: a dictionary of values for this object
        """
        result = dict()
        result['number'] = self.number
        return result

    def to_xml_doc(self) -> xml.etree.ElementTree.Element:
        """
        Return the contents of the returns_error object as a Godot documentation XML element

        :return: this return_errors object as a Godot XML element
        """
        base_element = self._to_xml()
        base_element.tag = 'returns_error'
        return base_element


class ClassDocTutorialLink(Zucaritas):
    """
    This class represents a model of the class doc's tutorial link element

    :param str text: The value of the text attribute for this element, in this case a tutorial link..
    :param str title: The value of the title attribute for this element.

    """
    __slots__ = ('text', 'title')
    text: str
    """URL link to the tutorial"""
    title: str
    """The title of the tutorial"""

    def __init__(self, text: str = None, title: str = None) -> None:
        self.text = text
        """URL link to the tutorial"""
        self.title = title
        """The title of the tutorial"""

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of this object.

        :return: a dictionary of values for this object
        """
        result = dict()
        if self.text is not None:
            result['text'] = self.text
        if self.title is not None:
            result['title'] = self.title
        return result

    def to_xml_doc(self) -> xml.etree.ElementTree.Element:
        """
        Return the contents of the tutorial link object as a Godot documentation XML element

        :return: this link object as a Godot XML element
        """
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
        """
        Returns a dictionary representation of this object.

        :return: a dictionary of values for this object
        """
        result = dict()
        result['returns_error'] = []
        for error in self.data:
            value = error.to_dict()
            print("Error Value:: " , value)
            result['returns_error'].append(error.to_dict())
        return result

    def to_xml_doc(self) -> list[xml.etree.ElementTree.Element]:
        """
        todo: fix missing implementation for this method
        :return:
        """
        elements = []
        for return_error in self.data:
            elements.append(return_error.to_xml_doc())
        return elements

    @classmethod
    def from_json(cls, json_str: str):
        return super().from_json(ClassDocReturnError, json_str)

    @classmethod
    def from_xml(cls,element: xml.etree.ElementTree.Element):
        initial_list = [ClassDocReturnError.from_xml(e) for e in element]
        return cls(initial_list)


class DocParameters(ModelCollection):
    def __init__(self, initlist=None):
        super().__init__(ClassDocParameter, initlist)

    def new(self, **kwargs) -> ClassDocParameter:
        parameter = ClassDocParameter(**kwargs)
        self.append(parameter)
        return parameter

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of this object.

        :return: a dictionary of values for this object
        """
        result = dict()
        result['parameters'] = []
        for parameter in self.data:
            result['parameters'].append(parameter.to_dict())
        return result

    def to_xml_doc(self) -> list[xml.etree.ElementTree.Element]:
        """
        Return the contents of this list of parameters, as a list of Godot XML param elements

        :return: this list object as a list of XML param elements
        """
        elements = []
        for parameter in self.data:
            elements.append(parameter.to_xml_doc())
        return elements

    @classmethod
    def from_json(cls, json_str: str):
        return super().from_json(ClassDocParameter, json_str)

    @classmethod
    def from_xml(cls,element: xml.etree.ElementTree.Element):
        initial_list = [ClassDocParameter.from_xml(e) for e in element]
        return cls(initial_list)


class DocTutorials(ModelCollection):
    def __init__(self, initlist=None):
        super().__init__(ClassDocTutorialLink, initlist)

    def new(self, **kwargs) -> ClassDocTutorialLink:
        link = ClassDocTutorialLink(**kwargs)
        self.append(link)
        return link

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of this object.

        :return: a dictionary of values for this object
        """
        result = dict()
        result['tutorials'] = []
        for parameter in self.data:
            result['tutorials'].append(parameter.to_dict())
        return result

    def to_xml_doc(self) -> xml.etree.ElementTree.Element:
        element = Et.Element('tutorials')
        for tutorial_link in self.data:
            element.append(tutorial_link.to_xml_doc())
        return element

    @classmethod
    def from_json(cls, json_str: str):
        return super().from_json(ClassDocTutorialLink, json_str)

    @classmethod
    def from_xml(cls,element: xml.etree.ElementTree.Element):
        initial_list = [ClassDocTutorialLink.from_xml(e) for e in element]
        return cls(initial_list)
