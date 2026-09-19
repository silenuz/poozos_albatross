
<a id="luckys_zephyr.MemberDefinitionModel"></a>

## MemberDefinitionModel Objects

```python
@dataclass(slots=True, kw_only=True)
class MemberDefinitionModel(BriefDescriptionModel, DetailedDescriptionModel)
```

Used to model data from the Doxygen XML Memberdef elements
todo: add missing elements, already have more than needed might as well complete it
  <xsd:element name="templateparamlist" type="templateparamlistType" minOccurs="0" />
  <xsd:element name="reimplements" type="reimplementType" minOccurs="0" maxOccurs="unbounded" />
  <xsd:element name="reimplementedby" type="reimplementType" minOccurs="0" maxOccurs="unbounded" />
  <xsd:element name="param" type="paramType" minOccurs="0" maxOccurs="unbounded" />
  <xsd:element name="requiresclause" type="linkedTextType" minOccurs="0" />
  <xsd:element name="exceptions" type="linkedTextType" minOccurs="0" />
  <xsd:element name="references" type="referenceType" minOccurs="0" maxOccurs="unbounded" />
  <xsd:element name="referencedby" type="referenceType" minOccurs="0" maxOccurs="unbounded" />

<a id="luckys_zephyr.MemberDefinitionModel.attributes"></a>

### [attributes](memberdef_attributes.md)

Doxygen element attributes for this member definition

<a id="luckys_zephyr.MemberDefinitionModel.name"></a>

### name

simple name portion of the method or member name

<a id="luckys_zephyr.MemberDefinitionModel.qualifiedname"></a>

### qualifiedname

qualified name of the method or member

<a id="luckys_zephyr.MemberDefinitionModel.definition"></a>

### definition

member definition data value followed by qualified name, ex: int Summator::get_total

<a id="luckys_zephyr.MemberDefinitionModel.type"></a>

### type

data type if a field the data type of the field, if a function the return type of the function

<a id="luckys_zephyr.MemberDefinitionModel.initializer"></a>

### initializer

the initialization value of a variable, macro, or property definition. It captures the = sign and everything after it (within the initialization syntax) in the source code.

<a id="luckys_zephyr.MemberDefinitionModel.argsstring"></a>

### argsstring

If applicable contains the argument string for the member

<a id="luckys_zephyr.MemberDefinitionModel.inbodydescription"></a>

### inbodydescription

Houses any documentation or comment text blocks found physically embedded inside the body implementation of a function or method block.

<a id="luckys_zephyr.MemberDefinitionModel.location"></a>

### [location](memberdef_location.md)

File path, line start, line end, and column information where the symbol is defined.

<a id="luckys_zephyr.MemberDefinitionModel.read"></a>

### read

Used for language properties (like C# properties) to identify the specific getter implementation or evaluation context.

<a id="luckys_zephyr.MemberDefinitionModel.write"></a>

### write

Used for language properties (like C# properties) to identify the specific setter implementation or evaluation context.

<a id="luckys_zephyr.MemberDefinitionModel.bitfield"></a>

### bitfield

The bit-width allocation layout expression string if the variable is declared as a C/C++ struct or class bit-field.

<a id="luckys_zephyr.MemberDefinitionModel.qualifier"></a>

### qualifier

Contains custom string labels or modifiers applied to the code member via the qualifier command.

<a id="luckys_zephyr.MemberDefinitionModel.enum_values"></a>

### enum\_values

if the member definition is an enumerator this list will contain the list of enumerator values

<a id="luckys_zephyr.MemberDefinitionModel.parameters"></a>

### parameters

if the member has parameters this this list will contain a list of parameter values

<a id="luckys_zephyr.MemberDefinitionModel.returns"></a>

### returns

if applicable a description of the return value for the member

<a id="luckys_zephyr.MemberDefinitionModel.initializer_value"></a>

### initializer\_value

```python
@property
def initializer_value() -> str
```

Get the content of the initializer after the equals sign.

**Returns**:

initializer value without the preceding equal sign