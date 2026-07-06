Zucaritas
=========

 Cereal base for top level objects, providing serialization and deserialization between XML and JSON,
for Godot documentation elements.

"Never get out of the boat!"

## Methods:

| Return | Name |
| --- | --- |
| None | from_json |  |
| str | to_json |  |
| str | get_inner_markup |  |
| None | from_xml |  |

## Method Descriptions:

### from_json

Create a model of this element from a JSON string

:param json_data: JSON string with element data
:return: A model of the element created from the JSON string
### to_json

Returns the model of this element as a JSON string

:return: A JSON string with element data
### get_inner_markup

Gets the text content of an XML element  by iterating the markup and creating a single
string

:param element: The element with .text content to parse
:return: a string with the text content of the element passed as an argument
### from_xml

Creates this model from a Godot class documentation XML element

:param element: The element represented by this model
:return: A model created from the XML documentation element