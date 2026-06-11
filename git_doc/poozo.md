Information:
============
This module contains the PoozoNotus class with methods for scraping source code files for GDExtension bindings, and returning the results
as a list composed of dataclasses that model the original data.

The data class definitions used by PoozoNotus methods are also defined in this module.

Usage:
======
Unfortunately neither the summator nor traffic light implementations are complete, traffic light has properties but no methods
and summator has methods but no properties, so I apologise for the samples switching between the different files.

All the usage samples are in the [poozo_sample.py](poozo_sample.py).

Get bound methods:
------------------
To get the bound methods that can be parsed use the ```get_bound_methods``` of the PoozoNotus class

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
