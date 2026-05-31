#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 5/28/26
@File: build_all

@Author: Silenuz Nowan (silenuznowan@yahoo.com)

Python module that uses Doxygen to document the example classes, using the example config
file in the config directory.  It then attempts to generate a build profile, and Godot class documentation from
the generated Doxygen content.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Get the absolute path to this script
script_path = Path(__file__).resolve()

# Get the absolute path to the directory containing the python scripts
spirare_script_dir = script_path.parent.parent / 'src' / 'spirare'
sys.path.append(str(spirare_script_dir))

# Check if Doxygen found in path
doxygen_path = shutil.which('doxygen')

if doxygen_path:
    # set the example directory as the working directory as the relative paths in the
    # Doxygen configuration file are relative to the working directory and not the
    # directory containing the configuration file.
    os.chdir(script_path.parent)
    doxygen_config_file = script_path.parent / 'config' / 'example_doxygen_config.cfg'
    has_config = False

    if not doxygen_config_file.exists():
        config_result = subprocess.run(["python3", "gen_doxygen_config.py"], capture_output=True, text=True)
        if config_result.returncode != 0:
            print("unable to generate a configuration for doxygen.  Doxygen can't run without a configuration file")
        else:
            has_config = True
    else:
        has_config = True

    if has_config:
        result = subprocess.run(["doxygen", "./config/example_doxygen_config.cfg"], capture_output=True, text=True)

        # uncomment the next line if you wish to see the output from doxygen, for example if there is a problem
        print(result.stdout)
        if result.returncode != 0:
            print(
                "Doxygen generation failed, depending on the state of the output data, the next steps may fail unexpectedly")
else:
    print("Doxygen not found in system path, unable to generate Doxygen XML")

# path to profile generator script
waft_gogo_path = spirare_script_dir / 'waft_gogo.py'

# profile generator needs two arguments, where to look for the doxygen content
# and where to put the build_profile_gen.json file, for this example
# the build profile will be generated in the example directory.
doxygen_xml_output = script_path.parent / 'doxygen_output'

# run profile generator
result = subprocess.run(["python3", str(waft_gogo_path), str(doxygen_xml_output), str(script_path.parent)],
                        capture_output=True, text=True)

if result.returncode != 0:
    print("something went wrong while generating the build profile.")
    print(result.stdout)
else:
    print("Waft build profile generation succeeded")

# path to class documentation generator
aerify_didi_path = spirare_script_dir / "aerify_didi.py"

# class document generator needs two arguments, where to look for the doxygen content
# and where to put the generated class XML documentation, for this example
# the documentation is placed in the doc_classes_generated directory, doxygen xml output directory was set above
doc_classes_directory = script_path.parent / 'doc_classes_generated'

# run document generator
result = subprocess.run(["python3", str(aerify_didi_path), str(doxygen_xml_output), str(doc_classes_directory)],
                        capture_output=True, text=True)

if result.returncode != 0:
    print("something went wrong while generating the class documentation.")
    print(result.stdout)
else:
    print("Aerify class documentation generation succeeded")

# it doesn't matter how well you start if you fail to finish
print("Finished!")
