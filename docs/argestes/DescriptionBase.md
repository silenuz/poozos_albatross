# DescriptionBase
Module: argestes.doc_base


Base class for description elements such as description and brief_description


"1. Cover for me
 2. Oh, good idea boss!
 3. It was like that when I got here."

## Attributes / Parameters:

| Type | Name | Default |
| --- | --- | --- |
| str | [text](#text) |  |

## Methods:

| Return | Name |
| --- | --- |
| None | __init__ |  |
| None | __post_init__ |  |
| dict | to_dict |  |
| xml.etree.ElementTree.Element | to_xml_doc |  |
| None | from_xml |  |
| None | from_json |  |

## Attribute Descriptions:

### text

 the text value of the element

## Method Descriptions:

### __init__

Not Documented Yet
### __post_init__

Not Documented Yet
### to_dict

Returns a dictionary representation of this object.

:return: a dictionary of values for this object
### to_xml_doc

Return the contents of the description as a Godot documentation XML element

:return: this description object as a Godot XML element, the tag is based on the _element_name attribute
### from_xml

Creates a description object from a Godot XML element

:param element: The description or brief_description element to create the model from
:return: A new description object with the values from the Godot XML element
### from_json

Creates a description object from a JSON string

:param json_data: The description or brief_description JSON content to create the model from
:return: A new description object with the values from the JSON content
## Schema

