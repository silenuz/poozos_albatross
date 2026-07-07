ClassDocModel
=============

 This class represents a model of the root class element of the Godot doc xml.


"Your going to need a bigger boat"

## Attributes / Parameters:

| Type | Name | Default |
| --- | --- | --- |
| str | [name](#name) |  |
| [DocBriefDescription](./custom_lists/DocBriefDescription.md) | [brief_description](#brief_description) | DocBriefDescription() |
| [DocDescription](./custom_lists/DocDescription.md) | [description](#description) | DocDescription() |
| [DocAnnotations](./custom_lists/DocAnnotations.md) | [annotations](#annotations) | None |
| [DocConstants](./custom_lists/DocConstants.md) | [constants](#constants) | None |
| [DocConstructors](./custom_lists/DocConstructors.md) | [constructors](#constructors) | None |
| [DocMembers](./custom_lists/DocMembers.md) | [members](#members) | None |
| [DocMethods](./custom_lists/DocMethods.md) | [methods](#methods) | None |
| [DocOperators](./custom_lists/DocOperators.md) | [operators](#operators) | None |
| [DocSignals](./custom_lists/DocSignals.md) | [signals](#signals) | None |
| [DocThemeItems](./custom_lists/DocThemeItems.md) | [theme_items](#theme_items) | None |
| [DocTutorials](./custom_lists/DocTutorials.md) | [tutorials](#tutorials) | DocTutorials() |
| str | [inherits](#inherits) | None |
| str | [api_type](#api_type) | None |
| float | [version](#version) | None |
| bool | [is_deprecated](#is_deprecated) | None |
| bool | [is_experimental](#is_experimental) | None |
| str | [deprecated](#deprecated) | None |
| str | [experimental](#experimental) | None |
| str | [keywords](#keywords) | None |

## Methods:

| Return | Name |
| --- | --- |
| dict | to_dict |  |
| xml.etree.ElementTree.Element | to_xml_doc |  |
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

### to_dict

Returns a dictionary of the values for this class doc root element model instance.

:return: a dictionary of values for this class doc root model instance.
### to_xml_doc

Create a Godot class doc root element for this model instance.

:return: A Godot class doc root element for this model instance.
### from_file

Method Not Documented Yet