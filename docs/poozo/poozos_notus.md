<a id="poozos_notus"></a>

# poozos\_notus

Contains Data Transfer Objects for Godot

<a id="poozos_notus.PoozoNotus"></a>

## PoozoNotus Objects

```python
class PoozoNotus()
```

Class for parsing cpp source code to catalog any bindings.

"A boy's best friend is his mother"

<a id="poozos_notus.PoozoNotus.get_bound_enums"></a>

#### get\_bound\_enums

```python
def get_bound_enums() -> list[str]
```



<a id="poozos_notus.PoozoNotus.get_bound_methods"></a>

#### get\_bound\_methods

```python
def get_bound_methods() -> list[DMethodModel]
```



<a id="poozos_notus.PoozoNotus.get_bound_signals"></a>

#### get\_bound\_signals

```python
def get_bound_signals() -> list[MethodInfoModel]
```



<a id="poozos_notus.DMethodModel"></a>

## DMethodModel Objects

```python
@dataclass(slots=True)
class DMethodModel()
```

<a id="poozos_notus.DMethodModel.name"></a>

#### name

p_name value

<a id="poozos_notus.DMethodModel.class_name"></a>

#### class\_name

the name of the method's class

<a id="poozos_notus.DMethodModel.qualified_name"></a>

#### qualified\_name

the qualified name of the method

<a id="poozos_notus.DMethodModel.class_method"></a>

#### class\_method

actual name of the method in the class

<a id="poozos_notus.DMethodModel.args"></a>

#### args

p_arg list

<a id="poozos_notus.IntegerConstantModel"></a>

## IntegerConstantModel Objects

```python
@dataclass(slots=True)
class IntegerConstantModel()
```

Data Model to hold information about constant integer bindings in the source code.

<a id="poozos_notus.IntegerConstantModel.p_class"></a>

#### p\_class

p_class_name value

<a id="poozos_notus.IntegerConstantModel.p_enum"></a>

#### p\_enum

p_enum_value value

<a id="poozos_notus.IntegerConstantModel.p_name"></a>

#### p\_name

p_constant_name value

<a id="poozos_notus.IntegerConstantModel.p_value"></a>

#### p\_value

p_constant_value value

<a id="poozos_notus.IntegerConstantModel.p_is_bitfield"></a>

#### p\_is\_bitfield

is bitfield value

<a id="poozos_notus.MethodInfoModel"></a>

## MethodInfoModel Objects

```python
@dataclass(slots=True)
class MethodInfoModel()
```

MethodInfo Data Model

 Used to model a MethodInfo declaration in CPP code.

 CPP USAGE:
 1. Name only (No arguments, no return value / void)
       MethodInfo(const StringName &p_name);
2. Name followed by a variable number of PropertyInfo arguments(Used for signals and void methods)
      MethodInfo(const StringName &p_name, const PropertyInfo &p_p1);
      MethodInfo(const StringName &p_name, const PropertyInfo &p_p1, const PropertyInfo &p_p2);
3. Explicit Return Value FIRST, then Name, then arguments (Used for methods that return a value)
      MethodInfo(const PropertyInfo &p_return_val, const StringName &p_name);

<a id="poozos_notus.MethodInfoModel.name"></a>

#### name

name of signal or method

<a id="poozos_notus.MethodInfoModel.argument_info"></a>

#### argument\_info

p_arg list

<a id="poozos_notus.MethodInfoModel.return_info"></a>

#### return\_info

return value

<a id="poozos_notus.PropertyInfoModel"></a>

## PropertyInfoModel Objects

```python
@dataclass(slots=True)
class PropertyInfoModel()
```

PropertyInfo Data Model

In a Godot GDExtension, PropertyInfo is used to describe a property's type, name, hint, and usage flags so
the engine can properly display it in the Inspector

    :param variant_type: The Godot Variant::Type of the property (e.g., Variant::INT, Variant::STRING, Variant::VECTOR3)
    :type variant_type: str
    :param name: The name of the property as it will be accessed in GDScript and the editor
    :type name: str


<a id="poozos_notus.PropertyInfoModel.variant_type"></a>

#### variant\_type

The Godot Variant::Type of the property (e.g., Variant::INT, Variant::STRING, Variant::VECTOR3)

<a id="poozos_notus.PropertyInfoModel.name"></a>

#### name

The name of the property as it will be accessed in GDScript and the editor

<a id="poozos_notus.PropertyInfoModel.hint"></a>

#### hint

(Optional): A PropertyHint that tells the editor how to display or constrain the value (e.g., PROPERTY_HINT_RANGE, PROPERTY_HINT_ENUM).

<a id="poozos_notus.PropertyInfoModel.hint_string"></a>

#### hint\_string

(Optional): Extra information for the hint. For ranges, it's "min,max,step". For enums, it's a comma-separated list of names.

<a id="poozos_notus.PropertyInfoModel.usage_flags"></a>

#### usage\_flags

(Optional): A PropertyUsageFlags combination determining how the property behaves (e.g., PROPERTY_USAGE_DEFAULT, PROPERTY_USAGE_READ_ONLY).

<a id="poozos_notus.PropertyInfoModel.class_name"></a>

#### class\_name

(Optional): Used if the type is a Resource or Object and you want to specify the exact class type

<a id="poozos_notus.PropertyInfoModel.index"></a>

#### index

used to track the index of the model in the arg list

<a id="poozos_notus.PropertyInfoModel.from_arg_string"></a>

#### from\_arg\_string

```python
@classmethod
def from_arg_string(cls,
                    arg_string: str,
                    index: int = 0) -> "PropertyInfoModel"
```

Creates a PropertyInfo from a string containing the PropertyInfo arguments

**Arguments**:

- `index`: optional index to track the position of the property info, in a list or property info args
- `arg_string`: csv string containing the PropertyInfo arguments

**Returns**:

PropertyInfo

<a id="poozos_notus.PropertyModel"></a>

## PropertyModel Objects

```python
@dataclass(slots=True)
class PropertyModel()
```

Data Model for Bound properties parsed from source code

<a id="poozos_notus.PropertyModel.field"></a>

#### field

Member name

<a id="poozos_notus.PropertyModel.getter"></a>

#### getter

Name of the method to get the member value

<a id="poozos_notus.PropertyModel.setter"></a>

#### setter

Name of the method to set the member value

<a id="poozos_notus.PropertyModel.info"></a>

#### info

PropertyInfo model containing the information from the source code declaration

