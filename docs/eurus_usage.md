# Information
The eurus module contains the Eurus class which can act as a bridge between the Doxygen generated XML, and the
class docs model.

# Usage

To create a new Eurus object, instantiate it with the path to the GDExtension directory.  

```python
# set extension directory so that eurus can find the necessary source code to parse for bindings.
# use the same source code and generated doxygen xml as aerify does, (The example directory)
eurus = Eurus('somepath/poozos_albatross/example')
```
Using Eurus to generate standard class documentation from Doxygen XML is fairly basic.  
It can be used to process one Doxygen XML file to one ClassDocModel at a time, or it can be used
to create an ExtensionDocModel, containing a ClassDocModel for each processed Doxygen class
XML file.  

## ExtensionDocModel

When using Eurus to build the ExtensionDocModel, a GDExtension's class documentation can
be generated from the Doxygen XML in three lines of code.  Instantiate Eurus,
pass the directory path containing the Doxygen XML to Eurus' ```load_doxy_all``` method.

```python
eurus = Eurus('somepath/poozos_albatross/example')
## create a single ExtensionDocsModel using Eurus
## by passing the xml directory containing the doxygen generated xml
extension_docs = eurus.load_doxy_all(xml_directory=xml_folder)
## pass merge=False to overwrite any existing docs
extension_docs.save(target_directory=output_folder)
```

## ClassDocModel

When using Eurus to build individual ClassDocModel objects from each Doxygen class XML 
file, instantiate Eurus, and then get a list of Doxygen XML files, and pass the Doxygen XML
file path to Eurus' ```load_doxy``` method.

```python
eurus = Eurus('somepath/poozos_albatross/example')

## get list of doxygen class xml files
files = list(Path(xml_folder).rglob('class*.xml'))

## for each doxygen class XML file, create a model and from the model create a class doc XML file.
for file in files:
    # create model using doxygen XML
    class_doc = eurus.load_doxy(file)
    ## misname file so that it is not merged with in the later example.
    output_file_name = class_doc.name + '.xml'
    output_file = output_folder / output_file_name
    # create gd extension class doc XML from the model
    # if the file exists it will merge by default pass merge = false to overwrite existing class doc like:
    #class_doc.to_file(file_path=output_file,merge=False)
    class_doc.save(file_path=output_file)
```

All the above usage samples are in the [eurus_sample.py](../bin/eurus_sample.py).  

The sample script uses the examples
directory for parsing.