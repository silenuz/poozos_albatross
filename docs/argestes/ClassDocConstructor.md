# ClassDocConstructor


 
This class represents a model of the class docs constructor element



## Attributes / Parameters:

| Type | Name | Default |
| --- | --- | --- |
| str | [name](#name) |  |
| [Description](Description.md) | [description](#description) | Description() |
| str | [qualifiers](#qualifiers) | None |
| [DocParameters](./custom_lists/DocParameters.md) | [parameters](#parameters) | None |
| [ClassDocReturn](ClassDocReturn.md) | [return_value](#return_value) | None |

## Methods:

| Return | Name |
| --- | --- |
| None | __init__ |  |
| xml.etree.ElementTree.Element | to_xml_doc |  |

## Attribute Descriptions:

### name

 The value of the name attribute for the constructor element.
### description

 The value of the description element for the constructor element.
### qualifiers

 The value of the qualifiers attribute for the constructor element.
### parameters

 The value of the parameters element for the constructor element.
### return_value

 The value of the return_value element for the constructor element.

## Method Descriptions:

### __init__

Not Documented Yet
### to_xml_doc

Create a Godot class doc element for this constructor model instance.

:return: A Godot class doc element for this constructor model instance.
## Schema

The following schema definition is derived from Godot's main source repository, and is distributed under the MIT license.

Attribution: Juan Linietsky, Ariel Manzur and the Godot community

```xml
<xs:element  name="constructor" maxOccurs="unbounded" minOccurs="0">
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
        
```