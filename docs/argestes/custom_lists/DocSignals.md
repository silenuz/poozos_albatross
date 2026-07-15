DocSignals
==========

 This class models the signals [element](#schema), and contains a list of ClassDocSignal instances.


## Attributes / Parameters:

| Type | Name | Default |
| --- | --- | --- |
| list | [initlist](#initlist) | None |

## Methods:

| Return | Name |
| --- | --- |
| ClassDocSignal | new |  |
| dict | to_dict |  |
| xml.etree.ElementTree.Element | to_xml_doc |  |
| 'DocSignals' | from_json |  |
| None | from_xml |  |

## Attribute Descriptions:

### initlist

A list of ClassDocSignal instances.

## Method Descriptions:

### new

Creates a new ClassDocSignal instance and adds it to the list.

:param kwargs: Keyword arguments for the new ClassDocSignal instance.
:return: The new ClassDocSignal instance.
### to_dict

Returns a dictionary of the values for this signals' element model instance.

:return: a dictionary of values for this signals' model instance.
### to_xml_doc

Create a Godot class doc element for this signals list instance.

:return: A Godot class doc element for this signals list instance.
### from_json

Create a new DocSignals instance from a JSON string.

:param json_str: the JSON string containing the signals' data.
:return: A new DocSignals instance.
### from_xml

Method Not Documented Yet
## Schema

The following schema definition is derived from Godot's main source repository, and is distributed under the MIT license.

Attribution: Juan Linietsky, Ariel Manzur and the Godot community

```xml
<xs:element  name="signals" minOccurs="0">
    <xs:complexType>
        <xs:sequence>
            <xs:element name="signal" maxOccurs="unbounded" minOccurs="0">
                <xs:complexType>
                    <xs:sequence>
                        <xs:element name="param" maxOccurs="unbounded" minOccurs="0">
                            <xs:complexType>
                                <xs:sequence>
                                    <xs:sequence></xs:sequence>
                                </xs:sequence>
                                <xs:attribute type="xs:byte" name="index"></xs:attribute>
                                <xs:attribute type="xs:string" name="name"></xs:attribute>
                                <xs:attribute type="xs:string" name="type"></xs:attribute>
                                <xs:attribute type="xs:string" name="keywords" use="optional"></xs:attribute>
                            </xs:complexType>
                        </xs:element>
                        <xs:element type="xs:string" name="description"></xs:element>
                    </xs:sequence>
                    <xs:attribute type="xs:string" name="name" use="optional"></xs:attribute>
                    <xs:attribute type="xs:boolean" name="is_deprecated" use="optional"></xs:attribute>
                    <xs:attribute type="xs:boolean" name="is_experimental" use="optional"></xs:attribute>
                    <xs:attribute type="xs:string" name="deprecated" use="optional"></xs:attribute>
                    <xs:attribute type="xs:string" name="experimental" use="optional"></xs:attribute>
                </xs:complexType>
            </xs:element>
        </xs:sequence>
    </xs:complexType>
</xs:element>
                
```