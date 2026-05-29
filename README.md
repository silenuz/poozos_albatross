IMPORTANT
---------
Due to certain changes today, signal notes and warnings may be parsed as part of the class description
instead of as part of the signal description.  Should be fixed Monday which will mean working signal documentation generation.

Description:
------------
Some python scripts based off the Godot GDExtension cpp [template](https://github.com/godotengine/godot-cpp-template)
structure and build system to generate Godot class documentation from Doxygen generated XML.

While this project's source code is unlicensed, the doxygen.py module is not my work and is licensed
under the GNU Lesser General Public License version 2.1.  A copy of said license has been provided in the support directory.
This module can be used when using scons to build the Doxygen XML.  

Current Status: ALPHA (if that)
-------------------------------
Currently, the python script is capable of exporting the content for methods, properties, and enum constants.
Processing of signals is in progress and should be finished soon, as well code blocks in description fields should be working
in the next week or so. 

Contents:
---------
This repository contains 3 pythons scripts, one with shared functions, 
one for generating Godot class documentation from Doxygen generated XML files,
and one for generating a build_profile.json file for the project from the Doxygen
XML files.

The example directory has a self-contained example to represent parts of a GDExtension cpp template project.  It has
no requirement other than python, and contains command line scripts that demonstrate usage.

The example directory has a README with more information.

The support_files directory contains a sample cmake file for configuring Doxygen
and running the scripts as part of a cmake target.

The support files directory also contains Doxygen configuration file with
all the aliases already in it.  This can then be used from the command line to generate the
Doxygen XML so that the scripts can be used manually, or integrated into the scons build system via the doxygen.py module.

To see an example project using cmake with the scripts to generate Godot class documentation see 
[doxy_demo](https://github.com/silenuz/doxy_demo)

Notes:
------
There are multiple predefined aliases for Doxygen.  These aliases 
can be used in comments to insert Godot specific elements into the Doxygen XML output that will be ignored by other document 
generators like Breathe that work with the Doxygen XML output.  This output is also ignored when producing html, latex, 
or man pages documentation.

The Current Defined Aliases Are:
--------------------------------

Note the @signal, or \signal alias uses a pipe symbol | as the parameter seperator so that commas don't have to be escaped in the description.

It's also important not to use the built-in @warning or @note inside the description for a signal, as this will cause the 
Doxygen to create a paragraph outside the symbol description block, which will cause the parser to potentially include it as part
of the class description instead of the signal's description.

Lastly signals should be detailed in the detailed description area for the class.  This is where the parser looks.  If signals are
not described here, then the signal information output in the Godot docs will be the same empty structure that 
doctool produces.

 Aliases:

| Alias  | Action                          | Parameters | Example                    | Godot Output             | Standard Output       |
|--------|---------------------------------|------------|----------------------------|--------------------------|-----------------------|
| glnk   | Link to class                   | 1          | @glnk{class}               | [class]                  | class                 |
| gdcon  | Link to constant                | 2          | @gdcon{class,name}         | [constant class.name]    | name                  |
| gdenu  | Link to enum                    | 2          | @gdenu{class,name}         | [enum class.name]        | name                  |
| gdmem  | Link to member                  | 2          | @gdmem{class,name}         | [member class.name]      | name                  |
| gdmet  | Link to method                  | 2          | @gdmet{class,name}         | [method class.name]      | name                  |
| gdnew  | Link to built-in constructor    | 2          | @gdnew{class,name}         | [constructor class.name] | name                  |
| gdope  | Link to built-in operator       | 2          | @gdope{class,name}         | [operator class.name *]  | name                  |
| gdsig  | Link to signal                  | 2          | @gdsig{class,name}         | [signal class.name]      | name                  |
| gdthe  | Link to theme item              | 2          | @gdthe{class,name}         | [theme_item class.name]  | name                  |
| gdpar  | Parameter name as code          | 1          | @gdpar{name}               | [param name]             | name                  |
| signal | Creates a signal reference item | 2          | @signal{name\|description} | signal description       | signal reference item |
