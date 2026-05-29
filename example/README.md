This example represents some of the directories from the GDExtension templates directory structure.

* config: represents a tool directory, or config directory
* doc_classes_generated: this is where the Godot class XML is generated into
* doxygen_output: This is where Doxygen generated output ends up
* src: Represents the src directory in the template, this is what Doxygen will document.

The src directory contains two sample GDExtension classes, with comments to generate 
documentation from.

The doxygen_output directory has pre-generated Doxygen XML for the above classes so
this example can be run even if Doxygen is not present on the system.

If Doxygen is present the config directory has a Doxygen configuration file that can be used to generate 
a HTML sample if so desired.  As well if Doxygen is present, one can add additional classes to
the source directory to see what the generated documentation for those classes might look like.

To generate the Doxygen XML just open a terminal in the example directory and enter:
```commandline
doxygen ./config/doxygen_config.cfg 
```
This will generate the XML and HTML output files, and this read me should be the main page of the
HTML output.

There are three python scripts in the example directory as well.  

build_all will generate the Doxygen content if Doxygen can be found in the path, 
it will then generate a build profile, and class documentation.

gen_class_doc can be run from the command line to generate Godot class documentation in the doc_classes_generated 
directory.  This documentation is generated from the XML content in the doxygen_ouput directory.

gen_profile can also be run from the command line to generate a build profile for a GDExtension based on the content of
Doxygen generated XML.