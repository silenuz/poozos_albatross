# LuckyZephyr
Module: spirare.luckys_zephyr

This class provides some convenience methods for working with Doxygen generated XML.  The LuckyZephyr class has
a single parameter for instantiating, a Path object referencing the Doxygen class XML file to be processed.

[Sample Usage](../lucky_zephyr_usage.md)

Lucky Zephyr has the following attributes.

## Attributes:

| Type                          | Name           | Description                                                        |
|-------------------------------|----------------|--------------------------------------------------------------------|
| str                           | class_name     | The name of the class currently loaded                             |
| Path                          | class_xml      | The path to the Doxygen XML file                                   |
| xml.etree.ElementTree.Element | xml_root_node  | The root element of the Doxygen XML file                           |
| xml.etree.ElementTree.Element | data_node      | The class element of the Doxygen XML file                          |
| str| reference_file | The path to the reference XML file that contains extra information |
| dict | data_xml_map   | Map of each Doxygen XML element to it's parent element             |

## Methods:

### node\_from\_query

```python
def node_from_query(search_criteria: str) -> ElementTree.Element | None
```

Searches the Doxygen class XML for the first node meeting the XPath search criteria.

If found it returns the found node, else it returns None.

**Arguments**:

- `search_criteria`: the XPath search criteria

**Returns**:

the found node or None

<a id="luckys_zephyr.LuckyZephyr.node_from_attr"></a>

### node\_from\_attr

```python
def node_from_attr(attribute_name: str,
                   value: str) -> ElementTree.Element | None
```

Searches the Doxygen class XML for the first node that has a specific attribute value.

If found it returns the found node, else it returns None.

**Arguments**:

- `attribute_name`: the name of the attribute to search the value for
- `value`: the value to look for in the named attribute

**Returns**:

the found node or None

<a id="luckys_zephyr.LuckyZephyr.node_from_tag"></a>

### node\_from\_tag

```python
def node_from_tag(tag_name: str, value: str) -> ElementTree.Element | None
```

Searches the Doxygen class XML for the first node that has a specific tag value.

If found it returns the node, else it returns None.

**Arguments**:

- `tag_name`: the name of the tag to search for the value in
- `value`: the value of the tag being searched

**Returns**:

the found node or None

<a id="luckys_zephyr.LuckyZephyr.node_from_child_query"></a>

### node\_from\_child\_query

```python
def node_from_child_query(search: str) -> ElementTree.Element | None
```

Searches the Doxygen class XML for the first node meeting the XPath search criteria.

If found it returns the parent node of the found node, else it returns None.

**Arguments**:

- `search`: the XPath search criteria

**Returns**:

the parent node of the found node or None

<a id="luckys_zephyr.LuckyZephyr.node_from__child_attr"></a>

### node\_from\_\_child\_attr

```python
def node_from__child_attr(attribute_name: str,
                          value: str) -> ElementTree.Element | None
```

Searches the Doxygen class XML for the first node that has a specific attribute value.

If found it returns the parent node of the found node, else it returns None.

**Arguments**:

- `attribute_name`: the name of the attribute to search the value for
- `value`: the value to look for in the named attribute

**Returns**:

the parent node of the found node or None

<a id="luckys_zephyr.LuckyZephyr.node_from_child_tag"></a>

### node\_from\_child\_tag

```python
def node_from_child_tag(tag: str, value: str) -> ElementTree.Element | None
```

Searches the Doxygen class XML for the first node that has a specific tag value.

If found it returns the parent node of the found node, else it returns None.

**Arguments**:

- `tag`: the name of the tag to search for the value in
- `value`: the value of the tag being searched

**Returns**:

the parent node of the found node or None

<a id="luckys_zephyr.LuckyZephyr.get_class_description"></a>

### get\_class\_description

```python
def get_class_description(node_name: str) -> str
```

Gets either the class brief or detailed description depending on which node name is passed as an argument

Used by get_class_brief and get_class_detail.

**Arguments**:

- `node_name`: the name of the node to get the description for (briefdescription or detaileddescription).

**Returns**:

The inner XML content of the requested node

<a id="luckys_zephyr.LuckyZephyr.get_class_brief"></a>

### get\_class\_brief

```python
def get_class_brief() -> str
```

Gets the brief description of the class from the Doxygen class XML

**Returns**:

The inner XML content of the class's briefdescription node

<a id="luckys_zephyr.LuckyZephyr.get_class_detail"></a>

### get\_class\_detail

```python
def get_class_detail() -> str
```

Gets the detailed description of the class from the Doxygen class XML

**Returns**:

The inner XML content of the class's detaileddescription node

<a id="luckys_zephyr.LuckyZephyr.get_enumerator_data"></a>

### get\_enumerator\_data

```python
def get_enumerator_data(
        enumerator_value_name_list: list) -> list[EnumValueModel]
```

Iterates over the list of enumerator value names passed as an argument, it then gets the

reference file data and node map for the reference file, it then finds each
enumerator value name in the reference file XML tree, it then uses the parent child
XML map to get the enumerator-value element, and then the enumerator element from that.
Lastly it extracts the enumerator information to return to the calling function.

**Arguments**:

- `enumerator_value_name_list`: List of enumerator value names to search for

**Returns**:

A list of EnumValueModel containing the extracted information for each enumerator value

<a id="luckys_zephyr.LuckyZephyr.find_enumerator_value"></a>

### find\_enumerator\_value

```python
def find_enumerator_value(enumerator_value_name: str) -> EnumValueModel
```

Finds an enumerator value definition based on the name of the enumerator value

**Arguments**:

- `enumerator_value_name`: the name of the enumerator value to search for

**Returns**:

an EnumValueModel containing the extracted information
todo: check and see if logic error exists here (aug31)

<a id="luckys_zephyr.LuckyZephyr.get_include_values"></a>

### get\_include\_values

```python
def get_include_values() -> list[str]
```

**Returns**:

todo: this still has Godot specific code, needs to be removed for RC

<a id="luckys_zephyr.LuckyZephyr.get_methods"></a>

### get\_methods

```python
def get_methods(method_list: list) -> list[MemberDefinitionModel]
```

Iterates over the list of qualified names passed as an argument,

finding each in the current Doxygen XML tree, it then uses the parent child
XML map to get the parent node which is the member definition node, it then extracts member information
to return to the calling function.

**Arguments**:

- `method_list`: List of qualified names to search for

**Returns**:

A list of MemoryDefinitionModel containing the extracted information for each member

<a id="luckys_zephyr.LuckyZephyr.get_fields"></a>

### get\_fields

```python
def get_fields(member_list: list) -> list[MemberDefinitionModel]
```

Iterates over the list of member names passed as an argument,

finding each in the current Doxygen XML tree, it then uses the parent child
XML map to get the parent node which is the member definition node, it then extracts member information
to return to the calling function.

**Arguments**:

- `member_list`: List of member names to search for

**Returns**:

A list of MemberDefinitionModel containing the extracted information for each member

<a id="luckys_zephyr.LuckyZephyr.get_definitions"></a>

### get\_definitions

```python
def get_definitions(member_list: list,
                    tag_name: str) -> list[MemberDefinitionModel]
```

Iterates over the list of member's values passed as an argument,

finding each in the current Doxygen XML tree based on the tag vale specified in the tag_name
argument, it then uses the parent child XML map to get the parent node which is the member definition node, it then extracts member information
to return to the calling function.

**Arguments**:

- `member_list`: list of member values to be looked up
- `tag_name`: the name of the tag that should contain each member value

**Returns**:

A list of MemberDefinitionModel containing the extracted information for each member

<a id="luckys_zephyr.LuckyZephyr.find_by_name"></a>

### find\_by\_name

```python
def find_by_name(name: str) -> MemberDefinitionModel
```

Get a member definition based on the name of the member

**Arguments**:

- `name`: the name of the member

**Returns**:

a MemberDefinitionModel containing the extracted information

<a id="luckys_zephyr.LuckyZephyr.find_by_qualified"></a>

### find\_by\_qualified

```python
def find_by_qualified(qualified_name: str) -> MemberDefinitionModel
```

Get a member definition based on the qualified name of the member

**Arguments**:

- `qualified_name`: qualified name of the member

**Returns**:

a MemberDefinitionModel containing the extracted information

<a id="luckys_zephyr.LuckyZephyr.find_by_tag"></a>

### find\_by\_tag

```python
def find_by_tag(tag: str, value: str) -> MemberDefinitionModel
```

Get a member definition based on a specific tag value

**Arguments**:

- `tag`: the name of the tag that contains the search value
- `value`: the value being searched

**Returns**:

a MemberDefinitionModel containing the extracted information

<a id="luckys_zephyr.LuckyZephyr.map_parameter_descriptions"></a>

### map\_parameter\_descriptions

```python
def map_parameter_descriptions(
        param_values: list[ParameterTypeModel],
        param_description_node: ElementTree.Element) -> None
```

Doxygen stores the parameter list for relevant members in two places.  Each parameter is a param element of the

member node, with the descriptions for each parameter as part of a parameterlist node within the detaileddescritpion
node.  This method takes the descriptive content of the parameter values in the parameter list, and writes it to the
description value of the matching ParameterTypeModel.

**Arguments**:

- `param_values`: a list of ParameterTypeModel objects that need a description
- `param_description_node`: the parameterlist node from the detaileddescritpion node

**Returns**:

None

<a id="luckys_zephyr.LuckyZephyr.model_enumvalue_definition"></a>

### model\_enumvalue\_definition

```python
def model_enumvalue_definition(
        enum_value_node: ElementTree.Element) -> EnumValueModel
```

Takes an enumvalue element from the Doxygen XML as an argument and creates an EnumValueModel from it

**Arguments**:

- `enum_value_node`: the element to be modeled

**Returns**:

an EnumValueModel object

<a id="luckys_zephyr.LuckyZephyr.model_member_definition"></a>

### model\_member\_definition

```python
def model_member_definition(
        member_node: ElementTree.Element) -> MemberDefinitionModel
```

Takes a memberdef Doxygen XML element as an argument and creates an MemberDefinitionModel from it

**Arguments**:

- `member_node`: the element to be modeled

**Returns**:

a MemberDefinitionModel object

<a id="luckys_zephyr.LuckyZephyr.model_param_definition"></a>

### model\_param\_definition

```python
def model_param_definition(
        parameter_node: ElementTree.Element) -> ParameterTypeModel
```

Takes a param node from a memberdef element of the Doxygen XML and creates a ParameterTypeModel from it

**Arguments**:

- `parameter_node`: 

<a id="luckys_zephyr.LuckyZephyr.get_reference_file_path"></a>

### get\_reference\_file\_path

```python
def get_reference_file_path() -> Path
```

Trys to get the absolute path to the reference file containing extra header information.

**Returns**:

Absolute path to the reference file containing extra header information or None if not found

<a id="luckys_zephyr.LuckyZephyr.get_xref_items"></a>

### get\_xref\_items

```python
def get_xref_items(title: str) -> list[XRefSectionModel]
```

Gets all the xrefsections that match the title passed as an argument

**Arguments**:

- `title`: The heading or list title assigned to the cross-reference type to be retrieved.

**Returns**:

a list of XRefSectionModel objects

<a id="luckys_zephyr.LuckyZephyr.get_headlines_for_xrefitem"></a>

### get\_headlines\_for\_xrefitem

```python
def get_headlines_for_xrefitem(
        refitem: XRefSectionModel) -> list[SimpleSectionModel]
```

This method is specifically for use where a xrefitem uses a parblock container (like the custom Signal alias).

It can be used to get the parblock content that is not part of the xrefitem itself.

**Arguments**:

- `refitem`: The reference item to get the outer paragraphs for

**Returns**:

a list of SimpleSectionModel objects

<a id="luckys_zephyr.BriefDescriptionModel"></a>

## BriefDescriptionModel Objects

```python
@dataclass()
class BriefDescriptionModel()
```

<a id="luckys_zephyr.BriefDescriptionModel.briefdescription"></a>

### briefdescription

description of the method or member

<a id="luckys_zephyr.BriefDescriptionModel.text_brief_description"></a>

### text\_brief\_description

```python
@property
def text_brief_description() -> str
```

Get the plain text (removes html markup) from the brief description field


<a id="luckys_zephyr.BriefDescriptionModel.node_brief_description"></a>

### node\_brief\_description

```python
@property
def node_brief_description() -> ElementTree.Element
```

Get the brief description html and creates a node from it

**Returns**:

The node with the briefdescription markup as the text

<a id="luckys_zephyr.DetailedDescriptionModel"></a>

## DetailedDescriptionModel Objects

```python
@dataclass()
class DetailedDescriptionModel()
```

Model to hold description information, with convenience properties to get the content as an element
or as plain text without html markup

<a id="luckys_zephyr.DetailedDescriptionModel.description"></a>

### description

detailed description of the method or member

<a id="luckys_zephyr.DetailedDescriptionModel.text_description"></a>

### text\_description

```python
@property
def text_description() -> str
```

Get the plain text (removes html markup) from the detaileddescription field


<a id="luckys_zephyr.DetailedDescriptionModel.node_description"></a>

### node\_description

```python
@property
def node_description() -> ElementTree.Element
```

Get the detailed description html and creates a node from it

**Returns**:

The node with the detailed description markup as the text

<a id="luckys_zephyr.EnumValueAttributes"></a>

## EnumValueAttributes Objects

```python
@dataclass()
class EnumValueAttributes()
```

Data model for enumvalue tag attributes

<a id="luckys_zephyr.EnumValueAttributes.id"></a>

### id

A unique, auto-generated Doxygen identifier string used for cross-referencing throughout the XML structure

<a id="luckys_zephyr.EnumValueAttributes.prot"></a>

### prot

The access protection/visibility level in the source code. Possible values: public, protected, private,

<a id="luckys_zephyr.EnumValueModel"></a>

## EnumValueModel Objects

```python
@dataclass(slots=True, kw_only=True)
class EnumValueModel(BriefDescriptionModel, DetailedDescriptionModel)
```

Data model for enumvalue tag elements

<a id="luckys_zephyr.EnumValueModel.attributes"></a>

### attributes

Attributes for the tag

<a id="luckys_zephyr.EnumValueModel.name"></a>

### name

simple name portion of the method or member name

<a id="luckys_zephyr.EnumValueModel.initializer"></a>

### initializer

for constants and enumerators this indicates the initial value (includes the (equal) = sign.

<a id="luckys_zephyr.EnumValueModel.enum"></a>

### enum

Used to store parent enumerator name, not part of doxygen xsd

<a id="luckys_zephyr.EnumValueModel.initializer_value"></a>

### initializer\_value

```python
@property
def initializer_value() -> str
```

Get the content of the initializer after the equals sign.

**Returns**:

initializer value without the preceding equal sign




<a id="luckys_zephyr.ParameterTypeModel"></a>

## ParameterTypeModel Objects

```python
@dataclass(slots=True,kw_only=True)
class ParameterTypeModel(DetailedDescriptionModel)
```

Used to model data from the Doxygen XML param elements of the memberdef element
todo: make type an object so it can store refid child element if present (If the type references a known class or struct documented by Doxygen, it will include a <ref> child element
with a refid attribute pointing to that specific object's documentation.)

<a id="luckys_zephyr.ParameterTypeModel.attributes"></a>

### attributes

Captures any language-specific parameter attributes or modifiers, such as the keyword restrict in C or custom macro qualifiers

<a id="luckys_zephyr.ParameterTypeModel.type"></a>

### type

Contains the data type of the parameter (e.g., int, const char *).

<a id="luckys_zephyr.ParameterTypeModel.declname"></a>

### declname

The parameter's name as found in the declaration (e.g., in a header .h file).

<a id="luckys_zephyr.ParameterTypeModel.defname"></a>

### defname

The parameter's name as found in the definition (e.g., in a source .cpp file). This may differ or be identical to <declname>

<a id="luckys_zephyr.ParameterTypeModel.array"></a>

### array

If the parameter is a fixed-size or C-style array, this element captures the array dimensions (e.g., [3] or []).

<a id="luckys_zephyr.ParameterTypeModel.defval"></a>

### defval

Contains the default value assigned to the parameter if it is an optional parameter (e.g., = 0 or = nullptr).

<a id="luckys_zephyr.ParameterTypeModel.typeconstraint"></a>

### typeconstraint

It captures language-specific restrictions, interfaces, or constraints enforced on generic parameters or template types.

<a id="luckys_zephyr.XRefSectionModel"></a>

## XRefSectionModel Objects

```python
@dataclass(slots=True,kw_only=True)
class XRefSectionModel()
```

<a id="luckys_zephyr.XRefSectionModel.text_description"></a>

### text\_description

```python
@property
def text_description() -> str
```

Get the plain text (removes html markup) from the detaileddescription field


<a id="luckys_zephyr.XRefSectionModel.node_description"></a>

### node\_description

```python
@property
def node_description() -> ElementTree.Element
```

Get the detailed description html and creates a node from it

**Returns**:

The node with the detailed description markup as the text

