MethodReturnBase
================

 Base class extending MethodBase with a return element


" ‘To Start Press Any Key’. Where’s the ANY key?"

## Attributes / Parameters:

| Type | Name | Default |
| --- | --- | --- |
| str | [name](#name) |  |
| [DocDescription](./custom_lists/DocDescription.md) | [description](#description) | None |
| str | [qualifiers](#qualifiers) | None |
| [DocParameters](./custom_lists/DocParameters.md) | [parameters](#parameters) | None |
| [ClassDocReturn](ClassDocReturn.md) | [return_value](#return_value) | None |

## Methods:

| Return | Name |
| --- | --- |
| dict | to_dict |  |

## Attribute Descriptions:

### name

The value of the name attribute for this element.
### description

The value of the description element for this element.
### qualifiers

The value of the qualifiers attribute for this element.
### parameters

The value of the parameters element for this element.
### return_value

The value of the return_value element for this element.

## Method Descriptions:

### to_dict

Returns a dictionary representation of this object.

:return: a dictionary of values for this object