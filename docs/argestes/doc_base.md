# Module: `argestes.doc_base`

@Project: poozos_albatross
@Date: 6/21/26
@File: doc_base



## 📦 Class: `JsonBase`

#### 🛠️ Method: `JsonBase.from_json()`

#### 🛠️ Method: `JsonBase.to_json()`

## 📦 Class: `GodotBase`

#### 🛠️ Method: `GodotBase.get_inner_markup()`

#### 🛠️ Method: `GodotBase.from_xml()`

## 📦 Class: `DocQualifierBase`

Base class for elements with enum and is_bitfield attributes

* Parameter: **enum** 
	- Type: str 
	- Description:  enum attribute value
* Parameter: **is_bitfield** 
	- Type: bool 
	- Description:  is_bitfield attribute value

#### 🛠️ Method: `DocQualifierBase.to_dict()`

Returns a dictionary representation of this object.

:return: a dictionary of values for this object

## 📦 Class: `DescriptionBase`

Base class for description elements such as description and brief_description

* Parameter: **text** 
	- Type: str 
	- Description:  the text value of the element

#### 🛠️ Method: `DescriptionBase.to_dict()`

Returns a dictionary representation of this object.

:return: a dictionary of values for this object

#### 🛠️ Method: `DescriptionBase.to_xml_doc()`

Return the contents of the description as a Godot documentation XML element

:return: this description object as a Godot XML element, the tag is based on the _element_name attribute

#### 🛠️ Method: `DescriptionBase.from_xml()`

Creates a description object from a Godot XML element

:param element: The description or brief_description element to create the model from
:return: A new description object with the values from the Godot XML element

#### 🛠️ Method: `DescriptionBase.from_json()`

Creates a description object from a JSON string

:param json_data: The description or brief_description JSON content to create the model from
:return: A new description object with the values from the JSON content

## 📦 Class: `DocBriefDescription`

Model for brief_description elements

* Parameter: **text** 
	- Type: str 
	- Description:  the text value of the brief_description element

## 📦 Class: `DocDescription`

Model for description elements

* Parameter: **text** 
	- Type: str 
	- Description:  the text value of the description element

## 📦 Class: `MemberBase`

Base class extending qualifiers

* Parameter: **enum** 
	- Type: str 
	- Description:  The value of the enum attribute for this element.
* Parameter: **is_bitfield** 
	- Type: bool 
	- Description:  The value of the is_bitfield attribute for this element.
* Parameter: **name** 
	- Type: str 
	- Description:  The value of the name attribute for this element.
* Parameter: **text** 
	- Type: str 
	- Description:  The text value for this element.

#### 🛠️ Method: `MemberBase.to_dict()`

Returns a dictionary representation of this object.

:return: a dictionary of values for this object

## 📦 Class: `MemberBaseTags`

Base class extending MemberBase

* Parameter: **enum** 
	- Type: str 
	- Description:  The value of the enum attribute for this element.
* Parameter: **is_bitfield** 
	- Type: bool 
	- Description:  The value of the is_bitfield attribute for this element.
* Parameter: **name** 
	- Type: str 
	- Description:  The value of the name attribute for this element.
* Parameter: **text** 
	- Type: str 
	- Description:  The text value for this element.
* Parameter: **is_deprecated** 
	- Type: bool 
	- Description:  The value of the is_deprecated attribute for this element.
* Parameter: **is_experimental** 
	- Type: bool 
	- Description:  The value of the is_experimental attribute for this element.
* Parameter: **deprecated** 
	- Type: str 
	- Description:  The value of the deprecated attribute for this element.
* Parameter: **experimental** 
	- Type: str 
	- Description:  The value of the experimental attribute for this element.

#### 🛠️ Method: `MemberBaseTags.to_dict()`

Returns a dictionary representation of this object.

:return: a dictionary of values for this object

## 📦 Class: `ConstantMemberBase`

Base class extending MemberBaseTags

* Parameter: **enum** 
	- Type: str 
	- Description:  The value of the enum attribute for this element.
* Parameter: **is_bitfield** 
	- Type: bool 
	- Description:  The value of the is_bitfield attribute for this element.
* Parameter: **name** 
	- Type: str 
	- Description:  The value of the name attribute for this element.
* Parameter: **text** 
	- Type: str 
	- Description:  The value of the text attribute for this element.
* Parameter: **is_deprecated** 
	- Type: bool 
	- Description:  The value of the is_deprecated attribute for this element.
* Parameter: **is_experimental** 
	- Type: bool 
	- Description:  The value of the is_experimental attribute for this element.
* Parameter: **deprecated** 
	- Type: str 
	- Description:  The value of the deprecated attribute for this element.
* Parameter: **experimental** 
	- Type: str 
	- Description:  The value of the experimental attribute for this element.
* Parameter: **keywords** 
	- Type: str 
	- Description:  The value of the keywords attribute for this element.

#### 🛠️ Method: `ConstantMemberBase.to_dict()`

Returns a dictionary representation of this object.

:return: a dictionary of values for this object

## 📦 Class: `MethodBase`

Base class for method and method like elements

* Parameter: **name** 
	- Type: str 
	- Description:  The value of the name attribute for this element.
* Parameter: **description** 
	- Type: DocDescription 
	- Description:  The value of the description element for this element.
* Parameter: **qualifiers** 
	- Type: str 
	- Description:  The value of the qualifiers attribute for this element.
* Parameter: **parameters** 
	- Type: DocParameters 
	- Description:  The value of the parameters element for this element.

#### 🛠️ Method: `MethodBase.to_dict()`

Returns a dictionary representation of this object.

:return: a dictionary of values for this object

## 📦 Class: `MethodReturnBase`

Base class extending MethodBase with a return element

* Parameter: **name** 
	- Type: str 
	- Description:  The value of the name attribute for this element.
* Parameter: **description** 
	- Type: DocDescription 
	- Description:  The value of the description element for this element.
* Parameter: **qualifiers** 
	- Type: str 
	- Description:  The value of the qualifiers attribute for this element.
* Parameter: **parameters** 
	- Type: DocParameters 
	- Description:  The value of the parameters element for this element.
* Parameter: **return_value** 
	- Type: ClassDocReturn 
	- Description:  The value of the return_value element for this element.

#### 🛠️ Method: `MethodReturnBase.to_dict()`

Returns a dictionary representation of this object.

:return: a dictionary of values for this object

## 📦 Class: `ModelCollection`

A generic, reusable list that enforces types.  DO NOT USE DIRECTLY
if your expecting from_json to work as it's meant to return a subclass
of this class

#### 🛠️ Method: `ModelCollection.append()`

#### 🛠️ Method: `ModelCollection.insert()`

#### 🛠️ Method: `ModelCollection.to_json()`

#### 🛠️ Method: `ModelCollection.from_json()`

## 📦 Class: `ClassDocReturn`

This class represents a model of the method return element of the class docs
Note: type_value is used as the attribute here because type is a soft keyword in python.

* Parameter: **enum** 
	- Type: str 
	- Description:  The value of the enum attribute for return element.
* Parameter: **is_bitfield** 
	- Type: bool 
	- Description:  The value of the is_bitfield attribute for return element.
* Parameter: **type_value** 
	- Type: str 
	- Description:  The value of the type attribute for return element.

#### 🛠️ Method: `ClassDocReturn.to_dict()`

Returns a dictionary representation of this object.

:return: a dictionary of values for this object

#### 🛠️ Method: `ClassDocReturn.to_xml_doc()`

Return the contents of the return object as a Godot documentation XML element

:return: this return object as a Godot XML element

## 📦 Class: `ClassDocParameter`

This class represents a model of the class doc's parameter element, used in signals, methods, etc...

* Parameter: **enum** 
	- Type: str 
	- Description:  The value of the enum attribute for the parameter element.
* Parameter: **is_bitfield** 
	- Type: bool 
	- Description:  The value of the is_bitfield attribute for the parameter element.
* Parameter: **type_value** 
	- Type: str 
	- Description:  The value of the type_value attribute for the parameter element.
* Parameter: **index** 
	- Type: str 
	- Description:  The value of the index attribute for the parameter element.
* Parameter: **name** 
	- Type: str 
	- Description:  The value of the name attribute for the parameter element.
* Parameter: **default** 
	- Type: str 
	- Description:  The value of the default attribute for the parameter element.

#### 🛠️ Method: `ClassDocParameter.to_dict()`

Returns a dictionary representation of this object.

:return: a dictionary of values for this object

#### 🛠️ Method: `ClassDocParameter.to_xml_doc()`

Return the contents of the parameter (param) object as a Godot documentation XML element

:return: this parameter object as a Godot XML element

## 📦 Class: `ClassDocReturnError`

This class represents a model of the return error element of the class docs

* Parameter: **number** 
	- Type: int 
	- Description:  The value of the number attribute for this element.

#### 🛠️ Method: `ClassDocReturnError.to_dict()`

Returns a dictionary representation of this object.

:return: a dictionary of values for this object

#### 🛠️ Method: `ClassDocReturnError.to_xml_doc()`

Return the contents of the returns_error object as a Godot documentation XML element

:return: this return_errors object as a Godot XML element

## 📦 Class: `ClassDocTutorialLink`

This class represents a model of the class doc's tutorial link element

* Parameter: **text** 
	- Type: str 
	- Description:  The value of the text attribute for this element, in this case a tutorial link..
* Parameter: **title** 
	- Type: str 
	- Description:  The value of the title attribute for this element.

#### 🛠️ Method: `ClassDocTutorialLink.to_dict()`

Returns a dictionary representation of this object.

:return: a dictionary of values for this object

#### 🛠️ Method: `ClassDocTutorialLink.to_xml_doc()`

Return the contents of the tutorial link object as a Godot documentation XML element

:return: this link object as a Godot XML element

## 📦 Class: `DocReturnErrorsList`

#### 🛠️ Method: `DocReturnErrorsList.new()`

#### 🛠️ Method: `DocReturnErrorsList.to_dict()`

Returns a dictionary representation of this object.

:return: a dictionary of values for this object

#### 🛠️ Method: `DocReturnErrorsList.to_xml_doc()`

todo: fix missing implementation for this method
:return:

#### 🛠️ Method: `DocReturnErrorsList.from_json()`

#### 🛠️ Method: `DocReturnErrorsList.from_xml()`

## 📦 Class: `DocParameters`

#### 🛠️ Method: `DocParameters.new()`

#### 🛠️ Method: `DocParameters.to_dict()`

Returns a dictionary representation of this object.

:return: a dictionary of values for this object

#### 🛠️ Method: `DocParameters.to_xml_doc()`

Return the contents of this list of parameters, as a list of Godot XML param elements

:return: this list object as a list of XML param elements

#### 🛠️ Method: `DocParameters.from_json()`

#### 🛠️ Method: `DocParameters.from_xml()`

## 📦 Class: `DocTutorials`

todo: fix missing implementation for this method (to_xml doc)

#### 🛠️ Method: `DocTutorials.new()`

#### 🛠️ Method: `DocTutorials.to_dict()`

Returns a dictionary representation of this object.

:return: a dictionary of values for this object

#### 🛠️ Method: `DocTutorials.from_json()`

#### 🛠️ Method: `DocTutorials.from_xml()`

