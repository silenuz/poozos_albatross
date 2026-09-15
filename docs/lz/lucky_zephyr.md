# LuckyZephyr
Module: spirare.luckys_zephyr

This class provides some convenience methods for working with Doxygen generated XML.  The LuckyZephyr class has
a single parameter for instantiating, a Path object referencing the Doxygen class XML file to be processed.

[Sample Usage](../lucky_zephyr_usage.md)

Lucky Zephyr has the following attributes.

## Attributes:

| Type                          | Name           | Description                                                        |
|-------------------------------|----------------|--------------------------------------------------------------------|
| str                           | class_name     | The name of the class currently loaded                             |
| Path                          | class_xml      | The path to the Doxygen XML file                                   |
| xml.etree.ElementTree.Element | xml_root_node  | The root element of the Doxygen XML file                           |
| xml.etree.ElementTree.Element | data_node      | The class element of the Doxygen XML file                          |
| str| reference_file | The path to the reference XML file that contains extra information |
| dict | data_xml_map   | Map of each Doxygen XML element to it's parent element             |
