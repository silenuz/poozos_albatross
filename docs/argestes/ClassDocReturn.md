ClassDocReturn
==============

 This class represents a model of the method return [element](#schema) of the class docs
Note: type_value is used as the attribute here because type is a soft keyword in python.


## Attributes / Parameters:

| Type | Name | Default |
| --- | --- | --- |
| str | [enum](#enum) | None |
| bool | [is_bitfield](#is_bitfield) | None |
| str | [type_value](#type_value) | None |

## Methods:

| Return | Name |
| --- | --- |
| dict | to_dict |  |
| xml.etree.ElementTree.Element | to_xml_doc |  |

## Attribute Descriptions:

### enum

The value of the enum attribute for return element.
### is_bitfield

The value of the is_bitfield attribute for return element.
### type_value

The value of the type attribute for return element.

## Method Descriptions:

### to_dict

Returns a dictionary representation of this object.

:return: a dictionary of values for this object
### to_xml_doc

Return the contents of the return object as a Godot documentation XML element

:return: this return object as a Godot XML element
## Schema

