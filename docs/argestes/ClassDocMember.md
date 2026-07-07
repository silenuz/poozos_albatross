ClassDocMember
==============

 This class represents a model of the class doc's member element
    

"Open the pod bay doors, please, HAL"

## Attributes / Parameters:

| Type | Name | Default |
| --- | --- | --- |
| str | [enum](#enum) | None |
| bool | [is_bitfield](#is_bitfield) | None |
| str | [name](#name) |  |
| str | [text](#text) | None |
| bool | [is_deprecated](#is_deprecated) | None |
| bool | [is_experimental](#is_experimental) | None |
| str | [deprecated](#deprecated) | None |
| str | [experimental](#experimental) | None |
| str | [keywords](#keywords) | None |
| str | [type_value](#type_value) | None |
| str | [getter](#getter) | None |
| str | [setter](#setter) | None |
| str | [overrides](#overrides) | None |
| str | [default](#default) | None |

## Methods:

| Return | Name |
| --- | --- |
| dict | to_dict |  |
| xml.etree.ElementTree.Element | to_xml_doc |  |

## Attribute Descriptions:

### enum

The value of the enum attribute for the member element.
### is_bitfield

The value of the is_bitfield attribute for the member element.
### name

The value of the name attribute for the member element.
### text

The value of the text attribute for the member element.
### is_deprecated

The value of the is_deprecated attribute for the member element.
### is_experimental

The value of the is_experimental attribute for the member element.
### deprecated

The value of the deprecated attribute for the member element.
### experimental

The value of the experimental attribute for the member element.
### keywords

The value of the keywords attribute for the member element.
### type_value

The value of the type_value attribute for the member element.
### getter

The value of the getter attribute for the member element.
### setter

The value of the setter attribute for the member element.
### overrides

The value of the overrides attribute for the member element.
### default

The value of the default attribute for the member element.

## Method Descriptions:

### to_dict

Returns a dictionary of the values for this member element model instance.

:return: a dictionary of values for this member model instance.
### to_xml_doc

Create a Godot class doc element for this member model instance.

:return: A Godot class doc element for this member model instance.