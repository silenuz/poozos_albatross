#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 6/30/26
@File: zucaritas

This module contains the (cereal)serialization base

@Author:

Never get out of the boat.
"""
import json
import typing
from xml.etree import ElementTree as Et

class Zucaritas:
    # map of attributes that were renamed, currently just type is renamed because it shadows a soft keyword in python
    attribute_map = dict()
    attribute_map['type'] = 'type_value'

    @classmethod
    def from_json(cls, json_data):
        raw_args = json.loads(json_data)
        kwargs = {}
        for key, value in raw_args.items():
            attrib_type = typing.get_type_hints(cls).get(key)
            if attrib_type is not None and hasattr(attrib_type, 'from_json'):
                kwargs[key] = attrib_type.from_json(value)
            else:
                kwargs[key] = value

        return cls(**kwargs)

    def to_json(self):
        return json.dumps(self.to_dict())

    def get_inner_markup(self, element: Et.Element) -> str:
        # 1. Grab the initial text chunk before any child tag
        parts = [element.text or ""]
        for child in element:
            # encoding="unicode" returns a standard python string instead of bytes
            parts.append(Et.tostring(child, encoding="unicode"))
        return "".join(parts).strip()

    @classmethod
    def from_xml(cls, element: Et.Element):
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
            else:
                attr_type = class_object.__annotations__.get(e.tag)
                if attr_type is not None:
                    child = attr_type.from_xml(e)
                    setattr(class_object, e.tag, child)
        return class_object

    def _to_xml(self):
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
                    print(attr_type)
                    if attr_type == DocParameters:
                        params = attr_instance.to_xml_doc()
                        if isinstance(params, Et.Element):
                            element.append(params)
                        else:
                            for param in params:
                                print("append parameter")
                                element.append(param)
                    elif hasattr(attr_instance, 'to_xml_doc'):
                        print("append element")
                        sub_element = attr_instance.to_xml_doc()
                        element.append(sub_element)
                else:
                    print("key:: ", key)
                    element.set(key, str(value))
        return element