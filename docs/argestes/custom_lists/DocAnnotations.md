# DocAnnotations
Module: argestes.class_doc_annotation


This class models the annotations element, and contains a list of ClassDocAnnotation instances.



## Attributes / Parameters:

| Type | Name | Default |
| --- | --- | --- |
| list | [initlist](#initlist) | None |

## Methods:

| Return | Name |
| --- | --- |
| None | __init__ |  |
| ClassDocAnnotation | new |  |
| dict | to_dict |  |
| 'DocAnnotations' | from_json |  |
| xml.etree.ElementTree.Element | to_xml_doc |  |
| None | from_xml |  |

## Attribute Descriptions:

### initlist

 A list of ClassDocAnnotation instances.

## Method Descriptions:

### __init__

Not Documented Yet
### new

Creates a new ClassDocAnnotation instance and adds it to the list.

:param kwargs: Keyword arguments for the new ClassDocAnnotation instance.
:return: The new ClassDocAnnotation instance.
### to_dict

Returns a dictionary of the values for this annotations' element model instance.

:return: a dictionary of values for this annotations' model instance.
### from_json

Create a new DocAnnotations instance from a JSON string.

:param json_str: the JSON string containing the annotations' data.
:return: A new DocAnnotations instance.
### to_xml_doc

Create a Godot class doc element for this annotations list instance.

:return: A Godot class doc element for this annotations list instance.
### from_xml

Not Documented Yet
## Schema

The following schema definition is derived from Godot's main source repository, and is distributed under the MIT license.

Attribution: Juan Linietsky, Ariel Manzur and the Godot community

```xml
<xs:element  name="annotations" minOccurs="0">
    <xs:complexType>
        <xs:sequence>
            <xs:element name="annotation" maxOccurs="unbounded" minOccurs="0">
                <xs:complexType>
                    <xs:sequence>
                        <xs:element name="return" minOccurs="0">
                            <xs:complexType>
                                <xs:sequence>
                                    <xs:sequence></xs:sequence>
                                </xs:sequence>
                                <xs:attribute type="xs:string" name="type"></xs:attribute>
                                <xs:attribute type="xs:string" name="enum" use="optional"></xs:attribute>
                                <xs:attribute type="xs:boolean" name="is_bitfield" use="optional"></xs:attribute>
                            </xs:complexType>
                        </xs:element>
                        <xs:element name="param" maxOccurs="unbounded" minOccurs="0">
                            <xs:complexType>
                                <xs:sequence>
                                    <xs:sequence></xs:sequence>
                                </xs:sequence>
                                <xs:attribute type="xs:byte" name="index"></xs:attribute>
                                <xs:attribute type="xs:string" name="name"></xs:attribute>
                                <xs:attribute type="xs:string" name="type"></xs:attribute>
                                <xs:attribute type="xs:string" name="enum" use="optional"></xs:attribute>
                                <xs:attribute type="xs:boolean" name="is_bitfield" use="optional"></xs:attribute>
                                <xs:attribute type="xs:string" name="default" use="optional"></xs:attribute>
                            </xs:complexType>
                        </xs:element>
                        <xs:element type="xs:string" name="description"></xs:element>
                    </xs:sequence>
                    <xs:attribute type="xs:string" name="name" use="optional"></xs:attribute>
                    <xs:attribute type="xs:string" name="qualifiers" use="optional"></xs:attribute>
                    <xs:attribute type="xs:string" name="keywords" use="optional"></xs:attribute>
                </xs:complexType>
            </xs:element>
        </xs:sequence>
    </xs:complexType>
</xs:element>
                
```