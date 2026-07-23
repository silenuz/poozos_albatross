# ClassDocParameter


 
This class represents a model of the class doc's parameter element, used in signals, methods, etc...


## Attributes / Parameters:

| Type | Name | Default |
| --- | --- | --- |
| str | [enum](#enum) | None |
| bool | [is_bitfield](#is_bitfield) | None |
| str | [type_value](#type_value) | None |
| str | [index](#index) | None |
| str | [name](#name) |  |
| str | [default](#default) | None |

## Methods:

| Return | Name |
| --- | --- |
| None | __init__ |  |
| dict | to_dict |  |
| xml.etree.ElementTree.Element | to_xml_doc |  |

## Attribute Descriptions:

### enum

 The value of the enum attribute for the parameter element.
### is_bitfield

 The value of the is_bitfield attribute for the parameter element.
### type_value

 The value of the type_value attribute for the parameter element.
### index

 The value of the index attribute for the parameter element.
### name

 The value of the name attribute for the parameter element.
### default

 The value of the default attribute for the parameter element.

## Method Descriptions:

### __init__

Not Documented Yet
### to_dict

Returns a dictionary representation of this object.

:return: a dictionary of values for this object
### to_xml_doc

Return the contents of the parameter (param) object as a Godot documentation XML element

:return: this parameter object as a Godot XML element
## Schema

