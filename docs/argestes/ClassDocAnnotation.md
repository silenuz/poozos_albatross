ClassDocAnnotation
==================

 This class represents a model of the class docs annotation element


## Attributes / Parameters:

| Type | Name | Default |
| --- | --- | --- |
| str | [name](#name) |  |
| [DocDescription](./custom_lists/DocDescription.md) | [description](#description) | DocDescription() |
| str | [qualifiers](#qualifiers) | None |
| [DocParameters](./custom_lists/DocParameters.md) | [parameters](#parameters) | None |
| [ClassDocReturn](ClassDocReturn.md) | [return_value](#return_value) | None |
| str | [keywords](#keywords) | None |

## Methods:

| Return | Name |
| --- | --- |
| dict | to_dict |  |
| Element | to_xml_doc |  |

## Attribute Descriptions:

### name

The value of the name attribute for the annotation element.
### description

The value of the description element for the annotation element.
### qualifiers

The value of the qualifiers attribute for the annotation element.
### parameters

The value of the parameters element for the annotation element.
### return_value

The value of the return_value element for the annotation element.
### keywords

The value of the keywords attribute for the annotation element.

## Method Descriptions:

### to_dict

Returns a dictionary of the values for this annotation element model instance.

:return: a dictionary of values for this annotation model instance.
### to_xml_doc

Create a Godot class doc element for this annotation model instance.

Schema:

:return: