#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 7/17/26
@File: dynamo_docs

@Author: Silenuz Nowan (silenuznowan@yahoo.com)

New version of document generator for spirare and argestes.
"""
from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field
from pathlib import Path


# Get the absolute path to this script
script_path = Path(__file__).resolve()
PACKAGE_DIR = script_path.parent / 'spirare' / 'argestes'

########################################################################################################################
###                                          Data objects                                                            ###
########################################################################################################################

@dataclass
class DocAttribute:
    name: str
    description: str = ""
    type_value: str = ""
    default_value: str = ""

    @property
    def title(self):
        return f'[{self.name}](#{self.name})'

    @classmethod
    def from_ast(cls, value:str,class_name:str) -> DocAttribute:
        value = value.replace(":param ", "").strip()
        attribs = value.split(":")
        name = re.search(r'(\w+):', value).group(1)
        type = attribs[0].split(' ')[0]
        if type.startswith(("Class","Brief","Description")):
            if class_name.startswith("Doc"):
                type_value = f'[{type}](../{type}.md)'
            else:
                type_value = f'[{type}]({type}.md)'
        elif type.startswith("Doc"):
            if class_name.startswith("Doc"):
                type_value = f'[{type}]({type}.md)'
            else:
                type_value = f'[{type}](./custom_lists/{type}.md)'
        else:
            type_value = type
        description = attribs[1]
        return DocAttribute(name=name, type_value=type_value, description=description)

    def __eq__(self, other):
        if isinstance(other, DocAttribute):
            return  self.name == other.name
        return False


@dataclass
class DocArg:
    name: str
    description: str = ""
    type_value: str = ""
    default_value: str = ""


    def __eq__(self, other):
        if isinstance(other, DocAttribute):
            return  self.name == other.name
        return False

@dataclass
class DocMethod:
    name: str
    description: str = ""
    args: list[DocArg] = field(default_factory=list)

    @classmethod
    def from_ast(cls, ast_def: ast.FunctionDef) ->DocMethod:
        name = ast_def.name
        description = ast.get_docstring(ast_def)
        new_doc_method = cls(name=name, description=description)
        args_node = ast_def.args
        arg_count = len(args_node.args)
        default_arg_start_index = arg_count - len(args_node.defaults)

        for index in range(arg_count):
            arg_node = args_node.args[index]
            arg_name = arg_node.arg
            arg_type = ''
            if arg_node.annotation:
                arg_type = ast.unparse(arg_node.annotation)
            arg_default = ""
            if index >= default_arg_start_index:
                default_node = args_node.defaults[index - default_arg_start_index]
                if isinstance(default_node, ast.Constant):
                    arg_default = default_node.value
                else:
                    arg_default = ast.unparse(default_node)
            new_doc_method.args.append(DocArg(name=arg_name, type_value=arg_type, default_value=arg_default))
        return new_doc_method



@dataclass
class DocClass:
    name: str
    module_name: str
    description: str = ""
    doc_attributes: list[DocAttribute] = field(default_factory=list)
    doc_methods: list[DocMethod] = field(default_factory=list)

    @classmethod
    def from_ast(cls, class_def: ast.ClassDef, module_name:str= "") -> DocClass:
        name = class_def.name
        module_name = module_name
        doc_string = ast.get_docstring(class_def)
        new_class_doc = cls(name=name, module_name=module_name)
        if doc_string:
            new_class_doc.set_from_docstring(doc_string)
        for def_node in class_def.body:
            if isinstance(def_node, (ast.FunctionDef,ast.AsyncFunctionDef)):
                method_doc = DocMethod.from_ast(def_node)
                if method_doc.name.startswith("__init"):
                    for arg in method_doc.args:
                        if arg.default_value:
                            new_class_doc.set_default_attribute_value(arg.name, arg.default_value)
                new_class_doc.doc_methods.append(method_doc)
        return new_class_doc


    def set_from_docstring(self, docstring:str):
        values = docstring.split("\n")
        output: list[str] = []
        for value in values:
            if value.startswith('"') and value.endswith('"'):
                continue
            if value.startswith(':param'):
                doc_attribute = DocAttribute.from_ast(value, class_name=self.name)
                self.doc_attributes.append(doc_attribute)
            else:
               self.description += '\n' + value

    def set_default_attribute_value(self,attribute_name:str, value:str):
        attribute_match = next((attrib for attrib in self.doc_attributes if attrib.name == attribute_name), None)
        if attribute_match is not None:
            attribute_match.default_value = value

#######################################################################################################################
###                                         Generator                                                               ###
#######################################################################################################################

classes = dict()

def extract_docs_from_file(filepath: Path, rel_path: Path):
    """Parses a Python file using AST to extract module, class, and function docstrings."""
    try:
        node = ast.parse(filepath.read_text(encoding="utf-8"), filename=str(filepath))
    except (SyntaxError, UnicodeDecodeError):
        print('fubar file read ' , str(filepath))

    # Leave this for now, not sure I'll use the module level docstrings or not
    module_name = ".".join(rel_path.with_suffix("").parts)
    mod_doc = ast.get_docstring(node)

    # 2. Walk through top-level elements
    for child in node.body:
        # Classes
        if isinstance(child, ast.ClassDef):
            class_def = DocClass.from_ast(child,module_name)
            classes[class_def.name] = class_def


def generate_docs():
    pkg_path = PACKAGE_DIR

    if not pkg_path.exists():
        print(f"Error: Folder '{PACKAGE_DIR}' not found.")
        return

    for file_path in pkg_path.rglob("*.py"):
        if file_path.name.startswith("_"):
            continue

        # Get path relative to the parent of the package directory
        rel_path = file_path.relative_to(pkg_path.parent)
        extract_docs_from_file(file_path, rel_path)
    print(classes)
        #generate_output()

if __name__ == "__main__":
    generate_docs()


