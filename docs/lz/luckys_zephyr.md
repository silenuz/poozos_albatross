<a id="luckys_zephyr"></a>

# luckys\_zephyr

This module contains the [LuckyZephyr](lucky_zephyr.md) class that handles loading and parsing the Doxygen generated XML content.

In addition, it contains the response models for the relevant methods in the [LuckyZephyr](lucky_zephyr.md) class.

`Didi: "Tomorrow when I wake or think I do, what shall I say of today?
       That with Estragon my friend, at this place, until the fall of night, I waited for Godot? "`

## Functions

| Return | Name                                                                  |
|------- |-----------------------------------------------------------------------|
| ElementTree.Element | [get_inner_markup\(element:ElementTree.Element)](#get\_inner\_markup) | 
| str | [get_data_type(text:str)](#get\_data\_type)                           |  


## Objects

- [LuckyZephyr](lucky_zephyr.md) class 
- [MemberDefinitionModel](memberdef.md)
  - [MemberDefinitionAttributes](memberdef_attributes.md)
  - [MemberDefinitionlocation](memberdef_location.md)

## Function Descriptions:

<a id="luckys_zephyr.get_inner_markup"></a>

### get\_inner\_markup

```python
def get_inner_markup(element: ElementTree.Element) -> str
```

Gets the inner markup for the given element's text value, by concatenating the mixed element content into a single

XML string

**Arguments**:

- `element`: the element to get the inner markup for

**Returns**:

the full XML content of the text value of the element passed as an argument.

<a id="luckys_zephyr.get_data_type"></a>

### get\_data\_type

```python
def get_data_type(text) -> str
```

Parses text to determine the inner data type for Ref<data> text

**Returns**:

The inner data type for the text



