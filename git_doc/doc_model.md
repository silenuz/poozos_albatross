Introduction:
=============

The class documentation model is fairly simple in design.  Classes model elements, and class attributes are element attributes.

There is an exception for type attributes, where type in the class documentation is mapped to type_value in the model, due to the
fact that type is a soft keyword in python.

Usage:
------
The model can be created from either an XML root element from the Godot class documentation, or from a JSON string.

It can also be created directly from the file.


Model Documentation:
--------------------

