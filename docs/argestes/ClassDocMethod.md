ClassDocMethod
==============

 This class represents a model of the class doc's method element


"Oh no it wasn't the airplanes.  It was Beauty that killed the Beast."

## Attributes / Parameters:

| Type | Name | Default |
| --- | --- | --- |
| str | [name](#name) |  |
| [DocDescription](./custom_lists/DocDescription.md) | [description](#description) | DocDescription() |
| str | [qualifiers](#qualifiers) | None |
| [DocParameters](./custom_lists/DocParameters.md) | [parameters](#parameters) | None |
| [ClassDocReturn](ClassDocReturn.md) | [return_value](#return_value) | None |
| str | [keywords](#keywords) | None |
| [DocReturnErrorsList](./custom_lists/DocReturnErrorsList.md) | [returns_errors](#returns_errors) | None |
| bool | [is_deprecated](#is_deprecated) | None |
| bool | [is_experimental](#is_experimental) | None |
| str | [deprecated](#deprecated) | None |
| str | [experimental](#experimental) | None |

## Methods:

| Return | Name |
| --- | --- |
| dict | to_dict |  |
| Et.Element | to_xml_doc |  |

## Attribute Descriptions:

### name

The value of the name attribute for the method element.
### description

The value of the description element for the method element.
### qualifiers

The value of the qualifiers attribute for the method element.
### parameters

The value of the parameters element for the method element.
### return_value

The value of the return_value element for the method element.
### keywords

The value of the keywords attribute for the method element.
### returns_errors

The value of the returns_errors element for the method element.
### is_deprecated

The value of the is_deprecated attribute for the method element.
### is_experimental

The value of the is_experimental attribute for the method element.
### deprecated

The value of the deprecated attribute for the method element.
### experimental

The value of the experimental attribute for the method element.