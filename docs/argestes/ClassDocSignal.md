ClassDocSignal
==============

 This class represents a model of the class doc's signal [element](#schema)



## Attributes / Parameters:

| Type | Name | Default |
| --- | --- | --- |
| str | [name](#name) |  |
| [DocDescription](./custom_lists/DocDescription.md) | [description](#description) | DocDescription() |
| str | [qualifiers](#qualifiers) | None |
| [DocParameters](./custom_lists/DocParameters.md) | [parameters](#parameters) | None |
| bool | [is_deprecated](#is_deprecated) | None |
| str | [deprecated](#deprecated) | None |
| bool | [is_experimental](#is_experimental) | None |
| str | [experimental](#experimental) | None |

## Methods:

| Return | Name |
| --- | --- |
| dict | to_dict |  |
| xml.etree.ElementTree.Element | to_xml_doc |  |

## Attribute Descriptions:

### name

The value of the name attribute for the signal element.
### description

The value of the description element for the signal element.
### qualifiers

The value of the qualifiers attribute for the signal element.
### parameters

The value of the parameters element for the signal element.
### is_deprecated

The value of the is_deprecated attribute for the signal element.
### deprecated

The value of the deprecated attribute for the signal element.
### is_experimental

The value of the is_experimental attribute for the signal element.
### experimental

The value of the experimental attribute for the signal element.

## Method Descriptions:

### to_dict

Returns a dictionary of the values for this signal element model instance.

:return: a dictionary of values for this signal model instance.
### to_xml_doc

Create a Godot class doc element for this signal model instance.

:return: A Godot class doc element for this signal model instance.
## Schema

The following schema definition is derived from Godot's main source repository, and is distributed under the MIT license.

Attribution: Juan Linietsky, Ariel Manzur and the Godot community

```xml
<xs:element  name="signal" maxOccurs="unbounded" minOccurs="0">
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
        
```