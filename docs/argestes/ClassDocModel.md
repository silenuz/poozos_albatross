# ClassDocModel


## Attributes / Parameters:

| Type | Name | Default |
| --- | --- | --- |
| str | name |  |
| [BriefDescription](BriefDescription.md) | brief_description | BriefDescription() |
| [Description](Description.md) | description | Description() |
| [DocAnnotations](./lists/DocAnnotations.md) | annotations | None |
| [DocConstants](./lists/DocConstants.md) | constants | None |
| [DocConstructors](./lists/DocConstructors.md) | constructors | None |
| [DocMembers](./lists/DocMembers.md) | members | None |
| [DocMethods](./lists/DocMethods.md) | methods | None |
| [DocOperators](./lists/DocOperators.md) | operators | None |
| [DocSignals](./lists/DocSignals.md) | signals | None |
| [DocThemeItems](./lists/DocThemeItems.md) | theme_items | None |
| [DocTutorials](./lists/DocTutorials.md) | tutorials | DocTutorials() |
| str | inherits | None |
| str | api_type | None |
| float | version | None |
| bool | is_deprecated | None |
| bool | is_experimental | None |
| str | deprecated | None |
| str | experimental | None |
| str | keywords | None |

## Methods:

| Return | Name |
| --- | --- |
| None | __init__ |  |
| None | __post_init__ |  |
| None | __merge_lists |  |
| dict | __merge_dict |  |
| dict | to_dict |  |
| xml.etree.ElementTree.Element | to_xml_doc |  |
| ClassDocModel | merge |  |
| 'ClassDocModel' | from_file |  |

## Attribute Descriptions:

### name

 The value of the name attribute for this class element.
### brief_description

 The value of the brief_description element for this class element.
### description

 The value of the description element for this class element.
### annotations

 The value of the annotations element for this class element.
### constants

 The value of the constants element for this class element.
### constructors

 The value of the constructors element for this class element.
### members

 The value of the members element for this class element.
### methods

 The value of the methods element for this class element.
### operators

 The value of the operators element for this class element.
### signals

 The value of the signals element for this class element.
### theme_items

 The value of the theme_items element for this class element.
### tutorials

 The value of the tutorials element for this class element.
### inherits

 The value of the inherits attribute for this class element.
### api_type

 The value of the api_type attribute for this class element.
### version

 The value of the version attribute for this class element.
### is_deprecated

 The value of the is_deprecated attribute for this class element.
### is_experimental

 The value of the is_experimental attribute for this class element.
### deprecated

 The value of the deprecated attribute for this class element.
### experimental

 The value of the experimental attribute for this class element.
### keywords

 The value of the keywords attribute for this class element.

## Method Descriptions:

### __init__

Not Documented Yet
### __post_init__

Not Documented Yet
### __merge_lists

Merges update_list into old_list.
Updates dictionaries with matching 'name' keys and appends new ones.
### __merge_dict

Merges the content of the dictionary with updates, into the original dictionary.

:param original_dict: The original dictionary of values
:param dict_with_updates:  The dictionary with updated values
:return: original dictionary with the updated values
### to_dict

Returns a dictionary of the values for this class doc root element model instance.

:return: a dictionary of values for this class doc root model instance.
### to_xml_doc

Create a Godot class doc root element for this model instance.

:return: A Godot class doc root element for this model instance.
### merge

Merge content of the new content model with the content of this model instance.

:param new_content_model: The ClassDocModel instance that contains teh new or updated information that is to be merged with
    this instance.
:return: A new ClassDocModel instance that contains the merged content.
### from_file

Not Documented Yet
## Schema

The following schema definition is derived from Godot's main source repository, and is distributed under the MIT license.

Attribution: Juan Linietsky, Ariel Manzur and the Godot community

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<xs:schema attributeFormDefault="unqualified" elementFormDefault="qualified"
           xmlns:xs="http://www.w3.org/2001/XMLSchema">
    <xs:element name="class">
        <xs:complexType>
            <xs:sequence>
                <xs:element type="xs:string" name="brief_description"/>
                <xs:element type="xs:string" name="description"/>
                <xs:element name="tutorials">
                    <xs:complexType>
                        <xs:sequence>
                            <xs:element name="link" maxOccurs="unbounded" minOccurs="0">
                                <xs:complexType>
                                    <xs:simpleContent>
                                        <xs:extension base="xs:string">
                                            <xs:attribute type="xs:string" name="title" use="optional"/>
                                        </xs:extension>
                                    </xs:simpleContent>
                                </xs:complexType>
                            </xs:element>
                        </xs:sequence>
                    </xs:complexType>
                </xs:element>
                <xs:element name="constructors" minOccurs="0">
                    <xs:complexType>
                        <xs:sequence>
                            <xs:element name="constructor" maxOccurs="unbounded" minOccurs="0">
                                <xs:complexType>
                                    <xs:sequence>
                                        <xs:element name="return" minOccurs="0">
                                            <xs:complexType>
                                                <xs:sequence>
                                                    <xs:sequence/>
                                                </xs:sequence>
                                                <xs:attribute type="xs:string" name="type"/>
                                                <xs:attribute type="xs:string" name="enum" use="optional"/>
                                                <xs:attribute type="xs:boolean" name="is_bitfield" use="optional"/>
                                            </xs:complexType>
                                        </xs:element>
                                        <xs:element name="param" maxOccurs="unbounded" minOccurs="0">
                                            <xs:complexType>
                                                <xs:sequence>
                                                    <xs:sequence/>
                                                </xs:sequence>
                                                <xs:attribute type="xs:byte" name="index"/>
                                                <xs:attribute type="xs:string" name="name"/>
                                                <xs:attribute type="xs:string" name="type"/>
                                                <xs:attribute type="xs:string" name="enum" use="optional"/>
                                                <xs:attribute type="xs:boolean" name="is_bitfield" use="optional"/>
                                                <xs:attribute type="xs:string" name="default" use="optional"/>
                                            </xs:complexType>
                                        </xs:element>
                                        <xs:element type="xs:string" name="description"/>
                                    </xs:sequence>
                                    <xs:attribute type="xs:string" name="name" use="optional"/>
                                    <xs:attribute type="xs:string" name="qualifiers" use="optional"/>
                                </xs:complexType>
                            </xs:element>
                        </xs:sequence>
                    </xs:complexType>
                </xs:element>
                <xs:element name="methods" minOccurs="0">
                    <xs:complexType>
                        <xs:sequence>
                            <xs:element name="method" maxOccurs="unbounded" minOccurs="0">
                                <xs:complexType>
                                    <xs:sequence>
                                        <xs:element name="return" minOccurs="0">
                                            <xs:complexType>
                                                <xs:sequence>
                                                    <xs:sequence/>
                                                </xs:sequence>
                                                <xs:attribute type="xs:string" name="type"/>
                                                <xs:attribute type="xs:string" name="enum" use="optional"/>
                                                <xs:attribute type="xs:boolean" name="is_bitfield" use="optional"/>
                                            </xs:complexType>
                                        </xs:element>
                                        <xs:element name="returns_error" maxOccurs="unbounded" minOccurs="0">
                                            <xs:complexType>
                                                <xs:sequence>
                                                    <xs:sequence/>
                                                </xs:sequence>
                                                <xs:attribute type="xs:byte" name="number"/>
                                            </xs:complexType>
                                        </xs:element>
                                        <xs:element name="param" maxOccurs="unbounded" minOccurs="0">
                                            <xs:complexType>
                                                <xs:sequence>
                                                    <xs:sequence/>
                                                </xs:sequence>
                                                <xs:attribute type="xs:byte" name="index"/>
                                                <xs:attribute type="xs:string" name="name"/>
                                                <xs:attribute type="xs:string" name="type"/>
                                                <xs:attribute type="xs:string" name="enum" use="optional"/>
                                                <xs:attribute type="xs:boolean" name="is_bitfield" use="optional"/>
                                                <xs:attribute type="xs:string" name="default" use="optional"/>
                                            </xs:complexType>
                                        </xs:element>
                                        <xs:element type="xs:string" name="description"/>
                                    </xs:sequence>
                                    <xs:attribute type="xs:string" name="name" use="optional"/>
                                    <xs:attribute type="xs:string" name="qualifiers" use="optional"/>
                                    <!-- deprecated -->
                                    <xs:attribute type="xs:boolean" name="is_deprecated" use="optional"/>
                                    <xs:attribute type="xs:boolean" name="is_experimental" use="optional"/>
                                    <!-- /deprecated -->
                                    <xs:attribute type="xs:string" name="deprecated" use="optional"/>
                                    <xs:attribute type="xs:string" name="experimental" use="optional"/>
                                    <xs:attribute type="xs:string" name="keywords" use="optional"/>
                                </xs:complexType>
                            </xs:element>
                        </xs:sequence>
                    </xs:complexType>
                </xs:element>
                <xs:element name="members" minOccurs="0">
                    <xs:complexType>
                        <xs:choice maxOccurs="unbounded" minOccurs="0">
                            <xs:element name="member">
                                <xs:complexType>
                                    <xs:simpleContent>
                                        <xs:extension base="xs:string">
                                            <xs:attribute type="xs:string" name="name"/>
                                            <xs:attribute type="xs:string" name="type"/>
                                            <xs:attribute type="xs:string" name="setter"/>
                                            <xs:attribute type="xs:string" name="getter"/>
                                            <xs:attribute type="xs:string" name="overrides" use="optional"/>
                                            <xs:attribute type="xs:string" name="enum" use="optional"/>
                                            <xs:attribute type="xs:boolean" name="is_bitfield" use="optional"/>
                                            <xs:attribute type="xs:string" name="default" use="optional"/>
                                            <!-- deprecated -->
                                            <xs:attribute type="xs:boolean" name="is_deprecated" use="optional"/>
                                            <xs:attribute type="xs:boolean" name="is_experimental" use="optional"/>
                                            <!-- /deprecated -->
                                            <xs:attribute type="xs:string" name="deprecated" use="optional"/>
                                            <xs:attribute type="xs:string" name="experimental" use="optional"/>
                                            <xs:attribute type="xs:string" name="keywords" use="optional"/>
                                        </xs:extension>
                                    </xs:simpleContent>
                                </xs:complexType>
                            </xs:element>
                        </xs:choice>
                    </xs:complexType>
                </xs:element>
                <xs:element name="signals" minOccurs="0">
                    <xs:complexType>
                        <xs:sequence>
                            <xs:element name="signal" maxOccurs="unbounded" minOccurs="0">
                                <xs:complexType>
                                    <xs:sequence>
                                        <xs:element name="param" maxOccurs="unbounded" minOccurs="0">
                                            <xs:complexType>
                                                <xs:sequence>
                                                    <xs:sequence/>
                                                </xs:sequence>
                                                <xs:attribute type="xs:byte" name="index"/>
                                                <xs:attribute type="xs:string" name="name"/>
                                                <xs:attribute type="xs:string" name="type"/>
                                                <xs:attribute type="xs:string" name="keywords" use="optional"/>
                                            </xs:complexType>
                                        </xs:element>
                                        <xs:element type="xs:string" name="description"/>
                                    </xs:sequence>
                                    <xs:attribute type="xs:string" name="name" use="optional"/>
                                    <!-- deprecated -->
                                    <xs:attribute type="xs:boolean" name="is_deprecated" use="optional"/>
                                    <xs:attribute type="xs:boolean" name="is_experimental" use="optional"/>
                                    <!-- /deprecated -->
                                    <xs:attribute type="xs:string" name="deprecated" use="optional"/>
                                    <xs:attribute type="xs:string" name="experimental" use="optional"/>
                                </xs:complexType>
                            </xs:element>
                        </xs:sequence>
                    </xs:complexType>
                </xs:element>
                <xs:element name="constants" minOccurs="0">
                    <xs:complexType>
                        <xs:sequence>
                            <xs:element name="constant" maxOccurs="unbounded" minOccurs="0">
                                <xs:complexType>
                                    <xs:simpleContent>
                                        <xs:extension base="xs:string">
                                            <xs:attribute type="xs:string" name="name"/>
                                            <xs:attribute type="xs:string" name="value"/>
                                            <xs:attribute type="xs:string" name="enum" use="optional"/>
                                            <xs:attribute type="xs:boolean" name="is_bitfield" use="optional"/>
                                            <!-- deprecated -->
                                            <xs:attribute type="xs:boolean" name="is_deprecated" use="optional"/>
                                            <xs:attribute type="xs:boolean" name="is_experimental" use="optional"/>
                                            <!-- /deprecated -->
                                            <xs:attribute type="xs:string" name="deprecated" use="optional"/>
                                            <xs:attribute type="xs:string" name="experimental" use="optional"/>
                                            <xs:attribute type="xs:string" name="keywords" use="optional"/>
                                        </xs:extension>
                                    </xs:simpleContent>
                                </xs:complexType>
                            </xs:element>
                        </xs:sequence>
                    </xs:complexType>
                </xs:element>
                <xs:element name="annotations" minOccurs="0">
                    <xs:complexType>
                        <xs:sequence>
                            <xs:element name="annotation" maxOccurs="unbounded" minOccurs="0">
                                <xs:complexType>
                                    <xs:sequence>
                                        <xs:element name="return" minOccurs="0">
                                            <xs:complexType>
                                                <xs:sequence>
                                                    <xs:sequence/>
                                                </xs:sequence>
                                                <xs:attribute type="xs:string" name="type"/>
                                                <xs:attribute type="xs:string" name="enum" use="optional"/>
                                                <xs:attribute type="xs:boolean" name="is_bitfield" use="optional"/>
                                            </xs:complexType>
                                        </xs:element>
                                        <xs:element name="param" maxOccurs="unbounded" minOccurs="0">
                                            <xs:complexType>
                                                <xs:sequence>
                                                    <xs:sequence/>
                                                </xs:sequence>
                                                <xs:attribute type="xs:byte" name="index"/>
                                                <xs:attribute type="xs:string" name="name"/>
                                                <xs:attribute type="xs:string" name="type"/>
                                                <xs:attribute type="xs:string" name="enum" use="optional"/>
                                                <xs:attribute type="xs:boolean" name="is_bitfield" use="optional"/>
                                                <xs:attribute type="xs:string" name="default" use="optional"/>
                                            </xs:complexType>
                                        </xs:element>
                                        <xs:element type="xs:string" name="description"/>
                                    </xs:sequence>
                                    <xs:attribute type="xs:string" name="name" use="optional"/>
                                    <xs:attribute type="xs:string" name="qualifiers" use="optional"/>
                                    <xs:attribute type="xs:string" name="keywords" use="optional"/>
                                </xs:complexType>
                            </xs:element>
                        </xs:sequence>
                    </xs:complexType>
                </xs:element>
                <xs:element name="theme_items" minOccurs="0">
                    <xs:complexType>
                        <xs:sequence>
                            <xs:element name="theme_item" maxOccurs="unbounded" minOccurs="0">
                                <xs:complexType>
                                    <xs:simpleContent>
                                        <xs:extension base="xs:string">
                                            <xs:attribute type="xs:string" name="name"/>
                                            <xs:attribute type="xs:string" name="data_type"/>
                                            <xs:attribute type="xs:string" name="type"/>
                                            <xs:attribute type="xs:string" name="default" use="optional"/>
                                            <xs:attribute type="xs:string" name="deprecated" use="optional"/>
                                            <xs:attribute type="xs:string" name="experimental" use="optional"/>
                                            <xs:attribute type="xs:string" name="keywords" use="optional"/>
                                        </xs:extension>
                                    </xs:simpleContent>
                                </xs:complexType>
                            </xs:element>
                        </xs:sequence>
                    </xs:complexType>
                </xs:element>
                <xs:element name="operators" minOccurs="0">
                    <xs:complexType>
                        <xs:sequence>
                            <xs:element name="operator" maxOccurs="unbounded" minOccurs="0">
                                <xs:complexType>
                                    <xs:sequence>
                                        <xs:element name="return" minOccurs="0">
                                            <xs:complexType>
                                                <xs:sequence>
                                                    <xs:sequence/>
                                                </xs:sequence>
                                                <xs:attribute type="xs:string" name="type"/>
                                                <xs:attribute type="xs:string" name="enum" use="optional"/>
                                                <xs:attribute type="xs:boolean" name="is_bitfield" use="optional"/>
                                            </xs:complexType>
                                        </xs:element>
                                        <xs:element name="param" maxOccurs="unbounded" minOccurs="0">
                                            <xs:complexType>
                                                <xs:sequence>
                                                    <xs:sequence/>
                                                </xs:sequence>
                                                <xs:attribute type="xs:byte" name="index"/>
                                                <xs:attribute type="xs:string" name="name"/>
                                                <xs:attribute type="xs:string" name="type"/>
                                                <xs:attribute type="xs:string" name="enum" use="optional"/>
                                                <xs:attribute type="xs:boolean" name="is_bitfield" use="optional"/>
                                                <xs:attribute type="xs:string" name="default" use="optional"/>
                                            </xs:complexType>
                                        </xs:element>
                                        <xs:element type="xs:string" name="description"/>
                                    </xs:sequence>
                                    <xs:attribute type="xs:string" name="name" use="optional"/>
                                    <xs:attribute type="xs:string" name="qualifiers" use="optional"/>
                                </xs:complexType>
                            </xs:element>
                        </xs:sequence>
                    </xs:complexType>
                </xs:element>
            </xs:sequence>
            <xs:attribute type="xs:string" name="name"/>
            <xs:attribute type="xs:string" name="inherits" use="optional"/>
            <xs:attribute type="xs:string" name="api_type" use="optional"/>
            <!-- deprecated -->
            <xs:attribute type="xs:float" name="version" use="optional"/>
            <xs:attribute type="xs:boolean" name="is_deprecated" use="optional"/>
            <xs:attribute type="xs:boolean" name="is_experimental" use="optional"/>
            <!-- /deprecated -->
            <xs:attribute type="xs:string" name="deprecated" use="optional"/>
            <xs:attribute type="xs:string" name="experimental" use="optional"/>
            <xs:attribute type="xs:string" name="keywords" use="optional"/>
        </xs:complexType>
    </xs:element>
</xs:schema>

```