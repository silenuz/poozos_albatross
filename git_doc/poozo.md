Information:
============
This module contains the PoozoNotus class with methods for scraping source code files for GDExtension bindings, and returning the results
as a list composed of dataclasses that model the original data.

The data class definitions used by PoozoNotus methods are also defined in this module.

Usage:
======
Unfortunately neither the summator nor traffic light implementations are complete, traffic light has properties but no methods
and summator has methods but no properties, so I apologise for the samples switching between the different files.

All the usage samples are in the [poozo_sample.py](poozo_sample.py).  The sample script uses the source code in the examples
directory for parsing.

Get bound methods:
------------------
To get the bound methods that can be parsed use the ```get_bound_methods``` of the PoozoNotus class.  This function
This method returns a list of [DMethodModel](#dmethodmodel) objects for those methods that could be parsed.

```python
# get bound methods that were bound using dmethod macro
# traffic light has no methods so we use summator here
bound_methods_set = summator_parser.get_bound_methods()
for bound_method in bound_methods_set:
    print(bound_method)
```
Outputs this:

```shell
DMethodModel(name='add', class_name=' Summator', qualified_name='&Summator::add', class_method='add', args=['value'])
DMethodModel(name='reset', class_name=' Summator', qualified_name='&Summator::reset', class_method='reset', args=[])
DMethodModel(name='get_total', class_name=' Summator', qualified_name='&Summator::get_total', class_method='get_total', args=[])
```

Get Bound Properties:
---------------------
To get the bound properties that can be parsed use the ```get_bound_properties``` of the PoozoNotus class
This method returns a list of [PropertyModel](#propertymodel) objects.

```python
# get bound properties, summator has no properties
# use traffic light source instead
bound_properties = traffic_light_parser.get_bound_properties()
for bound_property in bound_properties:
    print(bound_property)
```
Outputs this:

```shell
PropertyModel(field='go_texture', getter='get_go_texture', setter='set_go_texture', info=PropertyInfoModel(variant_type='Variant::OBJECT', name='go_texture', hint='PROPERTY_HINT_RESOURCE_TYPE', hint_string='Texture2D', usage_flags=None, class_name=None, index=0))
PropertyModel(field='caution_texture', getter='get_caution_texture', setter='set_caution_texture', info=PropertyInfoModel(variant_type='Variant::OBJECT', name='caution_texture', hint='PROPERTY_HINT_RESOURCE_TYPE', hint_string='Texture2D', usage_flags=None, class_name=None, index=0))
PropertyModel(field='stop_texture', getter='get_stop_texture', setter='set_stop_texture', info=PropertyInfoModel(variant_type='Variant::OBJECT', name='stop_texture', hint='PROPERTY_HINT_RESOURCE_TYPE', hint_string='Texture2D', usage_flags=None, class_name=None, index=0))
PropertyModel(field='light_type', getter='get_light_type', setter='set_light_type', info=PropertyInfoModel(variant_type='Variant::INT', name='light_type', hint='PROPERTY_HINT_ENUM', hint_string='Go,Caution,Stop', usage_flags=None, class_name=None, index=0))
```

Get Bound Signals:
------------------
To get the bound signals that can be parsed use the ```get_bound_signals``` of the PoozoNotus class
This method returns a list of [MethodInfoModel](#methodinfomodel) objects.

```python
# get bound signals, both files have signals, but traffic light has usage flags
bound_signals = traffic_light_parser.get_bound_signals()
for bound_signal in bound_signals:
    print(bound_signal)
```
Will output this:

```shell
MethodInfoModel(name='light_changed', argument_info=[PropertyInfoModel(variant_type='Variant::INT', name='light_type', hint='PROPERTY_HINT_NONE', hint_string='', usage_flags='PROPERTY_USAGE_DEFAULT | PROPERTY_USAGE_CLASS_IS_ENUM', class_name='TrafficLightType', index=0)], return_info=None)
MethodInfoModel(name='light_changing', argument_info=[PropertyInfoModel(variant_type='Variant::INT', name='current_light_type', hint='PROPERTY_HINT_NONE', hint_string='', usage_flags='PROPERTY_USAGE_DEFAULT|PROPERTY_USAGE_CLASS_IS_ENUM', class_name='TrafficLightType', index=0), PropertyInfoModel(variant_type='Variant::INT', name='new_light_type', hint='PROPERTY_HINT_NONE', hint_string='', usage_flags='PROPERTY_USAGE_DEFAULT|PROPERTY_USAGE_CLASS_IS_ENUM', class_name='TrafficLightType', index=1)], return_info=None)
```

Get Bound Integer Constants:
----------------------------
To get the bound integer constants that can be parsed use the ```get_bound_constants``` of the PoozoNotus class
This method returns list of [IntegerConstantModel](#integerconstantmodel) objects.

```python
## get bound integer constants
## recent refactors mean this method needs the name of the class to amp get_class_static() to
bound_integer_constants = summator_parser.get_bound_constants("Summator")
for bound_constant in bound_integer_constants:
    print(bound_constant)
```

```shell
IntegerConstantModel(p_class='Summator', p_enum='', p_name='SUM_REQUIRED', p_value='MINMUM_REQUIRED_AMOUNT', p_is_bitfield=False)
IntegerConstantModel(p_class='Summator', p_enum='', p_name='SUM_OKAY', p_value='DOING_OKAY_AMOUNT', p_is_bitfield=False)
IntegerConstantModel(p_class='Summator', p_enum='', p_name='SUM_GOOD', p_value='DOING_NOTHING_AMOUNT', p_is_bitfield=False)
```

Notes:
======

For the most part it should recognize multiline declarations even with inline comments, unless the comments have a closing bracket in them
```)``` , as this currently breaks the regex for the source code parser.

For example this is okay:

```cpp
ADD_SIGNAL(MethodInfo(
	   "light_changed",
	   PropertyInfo(
		   Variant::INT,                                       // 1. Data Type
		   "light_type",                                       // 2. Argument Name
		   PROPERTY_HINT_NONE,                                 // 3. Hint
		   "",                                                 // 4. Hint String
		   PROPERTY_USAGE_DEFAULT | PROPERTY_USAGE_CLASS_IS_ENUM, // 5. Enforce class enum usage
		   "TrafficLightType"                           // 6. Explicit Object Target String
	   )
   ));
```

But this is bad:

```cpp
ADD_SIGNAL(MethodInfo(
	   "light_changed",
	   PropertyInfo(
		   Variant::INT,                                       // 1. Data Type
		   "light_type",                                       // 2. Argument Name
		   PROPERTY_HINT_NONE,                                 // 3. Hint (supply inspector hint)
		   "",                                                 // 4. Hint String
		   PROPERTY_USAGE_DEFAULT | PROPERTY_USAGE_CLASS_IS_ENUM, // 5. Enforce class enum usage
		   "TrafficLightType"                           // 6. Explicit Object Target String
	   )
   ));
```

Data Models:
============
This section contains information about the fields and properties of the data classes returned by the various
class methods in PoozoNotus.

DMethodModel
------------
The DMethod model contains the following fields:

```python
name: str
"""p_name value"""
class_name: str
"""the name of the method's class"""
qualified_name: str
"""the qualified name of the method"""
class_method: str
"""actual name of the method in the class"""
args: List[str] = field(default_factory=list)
"""p_arg list"""
```
And one property ```qualified_method_name``` that returns the qualified name without the Address-Of operator.

IntegerConstantModel:
---------------------
This model has the following fields.

```python
p_class: str
"""p_class_name value"""
p_enum: str
"""p_enum_value value"""
p_name: str
"""p_constant_name value"""
p_value: str
"""p_constant_value value"""
p_is_bitfield: bool = False
"""is bitfield value"""
```

MethodInfoModel:
----------------
This model has the following fields, two of which use the [PropertyInfoModel](#propertyinfomodel)

```python
name: str
"""name of signal or method"""
argument_info: List[PropertyInfoModel] = field(default_factory=list)
"""p_arg list"""
return_info: PropertyInfoModel | None = None
"""return value"""
```

PropertyModel:
--------------
This model has the following fields.  
One of the fields is an object of type [PropertyInfoModel](#propertyinfomodel)

```python
field: str
"""Member name"""
getter: str
"""Name of the method to get the member value"""
setter: str
"""Name of the method to set the member value"""
info: PropertyInfoModel
"""PropertyInfo model containing the information from the source code declaration"""
```

PropertyInfoModel:
------------------
This model has the following fields.

```python
variant_type: str
"""The Godot Variant::Type of the property (e.g., Variant::INT, Variant::STRING, Variant::VECTOR3)"""
name: str
"""The name of the property as it will be accessed in GDScript and the editor"""
hint: str | None = None
"""(Optional): A PropertyHint that tells the editor how to display or constrain the value (e.g., PROPERTY_HINT_RANGE, PROPERTY_HINT_ENUM)."""
hint_string: str | None = None
"""(Optional): Extra information for the hint. For ranges, it's "min,max,step". For enums, it's a comma-separated list of names."""
usage_flags: str | None = None
"""(Optional): A PropertyUsageFlags combination determining how the property behaves (e.g., PROPERTY_USAGE_DEFAULT, PROPERTY_USAGE_READ_ONLY)."""
class_name: str | None = None
""" (Optional): Used if the type is a Resource or Object and you want to specify the exact class type"""
index: int = 0
"""used to track the index of the model in the arg list"""
```