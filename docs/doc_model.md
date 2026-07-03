Model Overview
==============

The class documentation model is fairly basic in design.  Classes model elements, and class attributes are element attributes.

There is an exception for type attributes, where type in the class documentation is mapped to type_value in the model, due to the
fact that type is a soft keyword in python and parameters are stored as nested lists, otherwise the model trys to mirror the XML as much
as possible.

The model incorporates the entire XSD for the class documentation, even objects like constructors 
that would be rare in an extension. 

Usage:
------
The model can be created from either an XML root element from the Godot class documentation:

```python
from xml.etree import ElementTree as Et

tree = Et.parse(file_path)
root = tree.getroot()
class_doc_model = ClassDocModel.from_xml(root)
```

or from a JSON string (uses a Path object):

```python
 with open(file_path, "r", encoding="utf-8") as file:
    data = file_path.read_text()
    class_doc_model = ClassDocModel.from_json(data)
```

Either type source type can be read directly from a file using ```from_file(path)```.  If the extension is unrecognized it will 
raise a value error.

```python
class_doc_model = ClassDocModel.from_file(file)
```

Sample Script:
--------------
There is a sample script demonstrating the above usage of the model [here](../bin/model_sample.py). In the samples folder are
two godot class documentation files.  One for Summator and one for TrafficLight, these have the full XML content for 
the classes with the current properties not generated from source code, having been filled in by Godot's doctool.

Running the script should create an output folder, it should then dump both class files to JSON, after which it loads 
the new JSON files and creates a new XML class document from each of the JSON files.

Model Documentation:
--------------------

More here soon.
Some information [here](./argestes/class_doc.md)
