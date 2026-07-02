# Module: `argestes.doc_base`

@Project: poozos_albatross
@Date: 6/21/26
@File: doc_base

@Author: Silenuz Nowan (silenuznowan@yahoo.com)

## 📦 Class: `JsonBase`

## 📦 Class: `GodotBase`

## 📦 Class: `DocQualifierBase`

## 📦 Class: `DescriptionBase`

## 📦 Class: `DocBriefDescription`

## 📦 Class: `DocDescription`

## 📦 Class: `MemberBase`

## 📦 Class: `MemberBaseTags`

## 📦 Class: `ConstantMemberBase`

## 📦 Class: `MethodBase`

## 📦 Class: `MethodReturnBase`

## 📦 Class: `ModelCollection`

A generic, reusable list that enforces types.  DO NOT USE DIRECTLY
if your expecting from_json to work as it's meant to return a subclass
of this class

## 📦 Class: `ClassDocReturn`

This class represents a model of the method return element of the class docs
Note: type_value is used as the attribute here because type is a soft keyword in python.

:param str enum: The value of the enum attribute for return element.
:param bool is_bitfield: The value of the is_bitfield attribute for return element.
:param str type_value: The value of the type attribute for return element.

## 📦 Class: `ClassDocParameter`

This class represents a model of the class doc's parameter element, used in signals, methods, etc...

:param str enum: The value of the enum attribute for the parameter element.
:param bool is_bitfield: The value of the is_bitfield attribute for the parameter element.
:param str type_value: The value of the type_value attribute for the parameter element.
:param str index: The value of the index attribute for the parameter element.
:param str name: The value of the name attribute for the parameter element.
:param str default: The value of the default attribute for the parameter element.

## 📦 Class: `ClassDocReturnError`

This class represents a model of the return error element of the class docs

:param int number: The value of the number attribute for this element.

## 📦 Class: `ClassDocTutorialLink`

This class represents a model of the class doc's tutorial link element

:param str text: The value of the text attribute for this element, in this case a tutorial link..
:param str title: The value of the title attribute for this element.

## 📦 Class: `DocReturnErrorsList`

## 📦 Class: `DocParameters`

## 📦 Class: `DocTutorials`

