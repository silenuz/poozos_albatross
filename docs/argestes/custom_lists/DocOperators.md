# DocOperators
Module: argestes.class_doc_operator


This class models the operators element, and contains a list of ClassDocOperator instances.



## Attributes / Parameters:

| Type | Name | Default |
| --- | --- | --- |
| list | [initlist](#initlist) | None |

## Methods:

| Return | Name |
| --- | --- |
| None | __init__ |  |
| ClassDocOperator | new |  |
| dict | to_dict |  |
| xml.etree.ElementTree.Element | to_xml_doc |  |
| 'DocOperators' | from_json |  |
| None | from_xml |  |

## Attribute Descriptions:

### initlist

 A list of ClassDocOperator instances.

## Method Descriptions:

### __init__

Not Documented Yet
### new

Creates a new ClassDocOperator instance and adds it to the list.

:param kwargs: Keyword arguments for the new ClassDocOperator instance.
:return: The new ClassDocOperator instance.
### to_dict

Returns a dictionary of the values for this operators' element model instance.

:return: a dictionary of values for this operators' model instance.
### to_xml_doc

Create a Godot class doc element for this operators list instance.

:return: A Godot class doc element for this operators list instance.
### from_json

Create a new DocOperators instance from a JSON string.

:param json_str: the JSON string containing the operators' data.
:return: A new DocOperators instance.
### from_xml

Not Documented Yet
## Schema

The following schema definition is derived from Godot's main source repository, and is distributed under the MIT license.

Attribution: Juan Linietsky, Ariel Manzur and the Godot community

```xml
<xs:element  name="operators" minOccurs="0">
    <xs:complexType>
        <xs:sequence>
            <xs:element name="operator" maxOccurs="unbounded" minOccurs="0">
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
                </xs:complexType>
            </xs:element>
        </xs:sequence>
    </xs:complexType>
</xs:element>
            
```