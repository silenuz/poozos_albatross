Information:
------------
This module contains

Usage:
------




Notes:
------

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
