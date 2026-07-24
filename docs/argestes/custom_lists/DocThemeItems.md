# DocThemeItems
Module: argestes.class_doc_theme_item


This class models the theme_items element, and contains a list of ClassDocThemeItem instances.


“Did I ever tell you the definition of insanity?”

## Attributes / Parameters:

| Type | Name | Default |
| --- | --- | --- |
| list | [initlist](#initlist) | None |

## Methods:

| Return | Name |
| --- | --- |
| None | __init__ |  |
| ClassDocThemeItem | new |  |
| dict | to_dict |  |
| xml.etree.ElementTree.Element | to_xml_doc |  |
| 'DocThemeItems' | from_json |  |
| None | from_xml |  |

## Attribute Descriptions:

### initlist

 A list of ClassDocThemeItem instances.

## Method Descriptions:

### __init__

Not Documented Yet
### new

Creates a new ClassDocThemeItem instance and adds it to the list.

:param kwargs: Keyword arguments for the new ClassDocThemeItem instance.
:return: The new ClassDocThemeItem instance.
### to_dict

Returns a dictionary of the values for this theme_items' element model instance.

:return: a dictionary of values for this theme_items' model instance.
### to_xml_doc

Create a Godot class doc element for this theme_items list instance.

:return: A Godot class doc element for this theme_items list instance.
### from_json

Create a new DocThemeItems instance from a JSON string.

:param json_str: the JSON string containing the theme_items' data.
:return: A new DocThemeItems instance.
### from_xml

Not Documented Yet
## Schema

The following schema definition is derived from Godot's main source repository, and is distributed under the MIT license.

Attribution: Juan Linietsky, Ariel Manzur and the Godot community

```xml
<xs:element  name="theme_items" minOccurs="0">
    <xs:complexType>
        <xs:sequence>
            <xs:element name="theme_item" maxOccurs="unbounded" minOccurs="0">
                <xs:complexType>
                    <xs:simpleContent>
                        <xs:extension base="xs:string">
                            <xs:attribute type="xs:string" name="name"></xs:attribute>
                            <xs:attribute type="xs:string" name="data_type"></xs:attribute>
                            <xs:attribute type="xs:string" name="type"></xs:attribute>
                            <xs:attribute type="xs:string" name="default" use="optional"></xs:attribute>
                            <xs:attribute type="xs:string" name="deprecated" use="optional"></xs:attribute>
                            <xs:attribute type="xs:string" name="experimental" use="optional"></xs:attribute>
                            <xs:attribute type="xs:string" name="keywords" use="optional"></xs:attribute>
                        </xs:extension>
                    </xs:simpleContent>
                </xs:complexType>
            </xs:element>
        </xs:sequence>
    </xs:complexType>
</xs:element>
                
```