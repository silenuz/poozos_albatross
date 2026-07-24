# DocMembers
Module: argestes.class_doc_member


This class models the members element, and contains a list of ClassDocMember instances.



## Attributes / Parameters:

| Type | Name | Default |
| --- | --- | --- |
| list | [initlist](#initlist) | None |

## Methods:

| Return | Name |
| --- | --- |
| None | __init__ |  |
| ClassDocMember | new |  |
| dict | to_dict |  |
| xml.etree.ElementTree.Element | to_xml_doc |  |
| 'DocMembers' | from_json |  |
| None | from_xml |  |

## Attribute Descriptions:

### initlist

 A list of ClassDocMember instances.

## Method Descriptions:

### __init__

Not Documented Yet
### new

Creates a new ClassDocMember instance and adds it to the list.

:param kwargs: Keyword arguments for the new ClassDocMember instance.
:return: The new ClassDocMember instance.
### to_dict

Returns a dictionary of the values for this members' element model instance.

:return: a dictionary of values for this members' model instance.
### to_xml_doc

Create a Godot class doc element for this members list instance.

:return: A Godot class doc element for this members list instance.
### from_json

Create a new DocMembers instance from a JSON string.

:param json_str: the JSON string containing the members' data.
:return: A new DocMembers instance.
### from_xml

Not Documented Yet
## Schema

The following schema definition is derived from Godot's main source repository, and is distributed under the MIT license.

Attribution: Juan Linietsky, Ariel Manzur and the Godot community

```xml
<xs:element  name="members" minOccurs="0">
    <xs:complexType>
        <xs:choice maxOccurs="unbounded" minOccurs="0">
            <xs:element name="member">
                <xs:complexType>
                    <xs:simpleContent>
                        <xs:extension base="xs:string">
                            <xs:attribute type="xs:string" name="name"></xs:attribute>
                            <xs:attribute type="xs:string" name="type"></xs:attribute>
                            <xs:attribute type="xs:string" name="setter"></xs:attribute>
                            <xs:attribute type="xs:string" name="getter"></xs:attribute>
                            <xs:attribute type="xs:string" name="overrides" use="optional"></xs:attribute>
                            <xs:attribute type="xs:string" name="enum" use="optional"></xs:attribute>
                            <xs:attribute type="xs:boolean" name="is_bitfield" use="optional"></xs:attribute>
                            <xs:attribute type="xs:string" name="default" use="optional"></xs:attribute>
                            <xs:attribute type="xs:boolean" name="is_deprecated" use="optional"></xs:attribute>
                            <xs:attribute type="xs:boolean" name="is_experimental" use="optional"></xs:attribute>
                            <xs:attribute type="xs:string" name="deprecated" use="optional"></xs:attribute>
                            <xs:attribute type="xs:string" name="experimental" use="optional"></xs:attribute>
                            <xs:attribute type="xs:string" name="keywords" use="optional"></xs:attribute>
                        </xs:extension>
                    </xs:simpleContent>
                </xs:complexType>
            </xs:element>
        </xs:choice>
    </xs:complexType>
</xs:element>
                
```