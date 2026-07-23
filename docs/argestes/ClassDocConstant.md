# ClassDocConstant


 
This class represents a model of the godot docs constant element



## Attributes / Parameters:

| Type | Name | Default |
| --- | --- | --- |
| str | [enum](#enum) | None |
| bool | [is_bitfield](#is_bitfield) | None |
| str | [name](#name) |  |
| str | [text](#text) | None |
| bool | [is_deprecated](#is_deprecated) | None |
| bool | [is_experimental](#is_experimental) | None |
| str | [deprecated](#deprecated) | None |
| str | [experimental](#experimental) | None |
| str | [keywords](#keywords) | None |
| str | [value](#value) | None |

## Methods:

| Return | Name |
| --- | --- |
| None | __init__ |  |
| None | to_dict |  |
| xml.etree.ElementTree.Element | to_xml_doc |  |

## Attribute Descriptions:

### enum

 The value of the enum attribute for the constant element.
### is_bitfield

 The value of the is_bitfield attribute for the constant element.
### name

 The value of the name attribute for the constant element.
### text

 The value of the text attribute for the constant element.
### is_deprecated

 The value of the is_deprecated attribute for the constant element.
### is_experimental

 The value of the is_experimental attribute for the constant element.
### deprecated

 The value of the deprecated attribute for the constant element.
### experimental

 The value of the experimental attribute for the constant element.
### keywords

 The value of the keywords attribute for the constant element.
### value

 The value of the value attribute for the constant element.

## Method Descriptions:

### __init__

Not Documented Yet
### to_dict

Returns a dictionary of the values for this constant element model instance.

:return: a dictionary of values for this constant model instance.
### to_xml_doc

Create a Godot class doc element for this constant model instance.

:return: A Godot class doc element for this constant model instance.
## Schema

The following schema definition is derived from Godot's main source repository, and is distributed under the MIT license.

Attribution: Juan Linietsky, Ariel Manzur and the Godot community

```xml
<xs:element  name="constant" maxOccurs="unbounded" minOccurs="0">
    <xs:complexType>
        <xs:simpleContent>
            <xs:extension base="xs:string">
                <xs:attribute type="xs:string" name="name"></xs:attribute>
                <xs:attribute type="xs:string" name="value"></xs:attribute>
                <xs:attribute type="xs:string" name="enum" use="optional"></xs:attribute>
                <xs:attribute type="xs:boolean" name="is_bitfield" use="optional"></xs:attribute>
                <xs:attribute type="xs:boolean" name="is_deprecated" use="optional"></xs:attribute>
                <xs:attribute type="xs:boolean" name="is_experimental" use="optional"></xs:attribute>
                <xs:attribute type="xs:string" name="deprecated" use="optional"></xs:attribute>
                <xs:attribute type="xs:string" name="experimental" use="optional"></xs:attribute>
                <xs:attribute type="xs:string" name="keywords" use="optional"></xs:attribute>
            </xs:extension>
        </xs:simpleContent>
    </xs:complexType>
</xs:element>
        
```