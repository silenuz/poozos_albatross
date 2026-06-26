#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 5/29/26
@File: gen_example_config

@Author: Silenuz Nowan (silenuznowan@yahoo.com)
"""
import configparser
import os
import shutil
import subprocess
from pathlib import Path

# Get the absolute path to this script
script_path = Path(__file__).resolve()

# set the example directory as the working directory as the relative paths in the
# Doxygen configuration file are relative to the working directory and not the
# directory containing the configuration file.  This holds true for the ini as well.
os.chdir(script_path.parent)

config = configparser.ConfigParser()
config.read('./config/example_config.ini')
config_values = dict()
config_value = dict()
config_value['input'] = 'PROJECT_NAME           = "My Project"'
config_value['output'] = 'PROJECT_NAME          = ' + config.get('Settings','project')
config_values["project"]  = config_value
config_value = dict()
config_value["input"] = 'OUTPUT_DIRECTORY       ='
config_value["output"] = 'OUTPUT_DIRECTORY      = ' + config.get('Settings','output')
config_values['output'] = config_value
config_value = dict()
config_value['input'] = 'INPUT                  ='
config_value['output'] = 'INPUT              = ' + config.get('Settings','input')
config_values["input"] = config_value
config_value = dict()
config_value["input"] = 'USE_MDFILE_AS_MAINPAGE ='
config_value["output"] = 'USE_MDFILE_AS_MAINPAGE =' + config.get('Settings','mdfile')
config_values['mdfile'] = config_value
config_value = dict()
config_value["input"] = 'GENERATE_XML           = NO'
config_value["output"] = 'GENERATE_XML          = ' + config.get('Settings','xml')
config_values['xml'] = config_value
config_value = dict()
config_value['input'] = 'GENERATE_HTML          = YES'
config_value['output'] = 'GENERATE_HTML          = ' + config.get('Settings','html')
config_values['html'] = config_value
config_value = dict()
config_value["input"] = 'GENERATE_LATEX         = YES'
config_value["output"] = 'GENERATE_LATEX          = ' + config.get('Settings','latex')
config_values['latex'] = config_value
config_value = dict()
config_value["input"] = 'GENERATE_MAN           = NO'
config_value["output"] = 'GENERATE_MAN          = ' + config.get('Settings','man')
config_values['man'] = config_value
config_value = dict()
config_value["input"] = 'RECURSIVE              = NO'
config_value["output"] = 'RECURSIVE              = ' + config.get('Settings','recursive')
config_values['recursive'] = config_value

# Check if Doxygen found in path
doxygen_path = shutil.which('doxygen')


if doxygen_path is None:
    print("Doxygen not found in system path, unable to generate Doxygen configuration file")
else:
    result = subprocess.run(["doxygen", "-s", "-g", "./config/tmp_config.tmp"], capture_output=True, text=True)
    # uncomment the next line if you wish to see the output from doxygen, for example if there is a problem
    #print(result.stdout)
    if result.returncode != 0:
        print("Doxygen seems to have failed to create an initial configuration to modify. Exiting...")
    else:
        initial_config_file = script_path.parent / "config" / "tmp_config.tmp"
        if initial_config_file.exists():
            initial_config = initial_config_file.read_text()
            initial_config = initial_config.replace(config_values['project']['input'],config_values['project']['output'])
            initial_config = initial_config.replace(config_values['output']['input'], config_values['output']['output'])
            initial_config = initial_config.replace(config_values['input']['input'], config_values['input']['output'])
            initial_config = initial_config.replace(config_values['mdfile']['input'], config_values['mdfile']['output'])
            initial_config = initial_config.replace(config_values['xml']['input'], config_values['xml']['output'])
            initial_config = initial_config.replace(config_values['html']['input'], config_values['html']['output'])
            initial_config = initial_config.replace(config_values['latex']['input'], config_values['latex']['output'])
            initial_config = initial_config.replace(config_values['man']['input'], config_values['man']['output'])
            initial_config = initial_config.replace(config_values['recursive']['input'], config_values['recursive']['output'])
            alias_file = script_path.parent.parent / "support_files" / "doxygen_aliases.txt"
            if not alias_file.exists():
                print("Could not find alias file. Unable to add custom aliases to the configuration file")
            else:
                aliases = alias_file.read_text()
                initial_config = initial_config.replace('ALIASES                =',aliases)

    ok = False

    try:
        with open("./config/example_doxygen_config.cfg", "w") as f:
            f.write(initial_config)
            ok = True
    except PermissionError:
        print(f"Error: You do not have permission to write to the config directory.")
    except OSError as e:
        print(f"An OS error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    if(ok == True):
        os.remove("./config/tmp_config.tmp")
        print("Doxygen configuration generation successful")
    else:
        print("Doxygen configuration generation failed, an initial config file was created but could not be altered, it may have to be hand edited.")

    print("Finished")