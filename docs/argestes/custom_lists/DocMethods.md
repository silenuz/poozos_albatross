DocMethods
==========

 This class models the methods element, and contains a list of ClassDocMethod instances.


## Attributes / Parameters:

| Type | Name | Default |
| --- | --- | --- |
| list | [initlist](#initlist) | None |

## Methods:

| Return | Name |
| --- | --- |
| ClassDocMethod | new |  |
| dict | to_dict |  |
| xml.etree.ElementTree.Element | to_xml_doc |  |
| 'DocMethods' | from_json |  |
| None | from_xml |  |

## Attribute Descriptions:

### initlist

A list of ClassDocMethod instances.

## Method Descriptions:

### new

Creates a new ClassDocMethod instance and adds it to the list.

:param kwargs: Keyword arguments for the new ClassDocMethod instance.
:return: The new ClassDocMethod instance.
### to_dict

Returns a dictionary of the values for this methods' element model instance.

:return: a dictionary of values for this methods' model instance.
### to_xml_doc

Create a Godot class doc element for this methods list instance.

:return: A Godot class doc element for this methods list instance.
### from_json

Create a new DocMethods instance from a JSON string.

:param json_str: the JSON string containing the methods' data.
:return: A new DocMethods instance.
### from_xml

Method Not Documented Yet
## Schema

The following schema definition is derived from Godot's main source repository, and is distributed under the MIT license.

Attribution: Juan Linietsky, Ariel Manzur and the Godot community

```xml
<xs:element  name="methods" minOccurs="0">
    <xs:complexType>
        <xs:sequence>
            <xs:element name="method" maxOccurs="unbounded" minOccurs="0">
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
                        <xs:element name="returns_error" maxOccurs="unbounded" minOccurs="0">
                            <xs:complexType>
                                <xs:sequence>
                                    <xs:sequence></xs:sequence>
                                </xs:sequence>
                                <xs:attribute type="xs:byte" name="number"></xs:attribute>
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
                    <xs:attribute type="xs:boolean" name="is_deprecated" use="optional"></xs:attribute>
                    <xs:attribute type="xs:boolean" name="is_experimental" use="optional"></xs:attribute>
                    <xs:attribute type="xs:string" name="deprecated" use="optional"></xs:attribute>
                    <xs:attribute type="xs:string" name="experimental" use="optional"></xs:attribute>
                    <xs:attribute type="xs:string" name="keywords" use="optional"></xs:attribute>
                </xs:complexType>
            </xs:element>
        </xs:sequence>
    </xs:complexType>
</xs:element>
                
```