ClassDocOperator
================

 This class represents a model of the class doc's operator element


"What we've got here is failure to communicate"

## Attributes / Parameters:

| Type | Name | Default |
| --- | --- | --- |
| str | [name](#name) |  |
| [DocDescription](./custom_lists/DocDescription.md) | [description](#description) | DocDescription() |
| str | [qualifiers](#qualifiers) | None |
| [DocParameters](./custom_lists/DocParameters.md) | [parameters](#parameters) | None |
| [ClassDocReturn](ClassDocReturn.md) | [return_value](#return_value) | None |

## Methods:

| Return | Name |
| --- | --- |
| xml.etree.ElementTree.Element | to_xml_doc |  |

## Attribute Descriptions:

### name

The value of the name attribute for the operator element.
### description

The value of the description element for the operator element.
### qualifiers

The value of the qualifiers attribute for the operator element.
### parameters

The value of the parameters element for the operator element.
### return_value

The value of the return_value element for the operator element.

## Method Descriptions:

### to_xml_doc

Create a Godot class doc element for this operator model instance.

:return: A Godot class doc element for this operator model instance.