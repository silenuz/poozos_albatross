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
PACKAGE_DIR = script_path.parent / 'spirare'

classes = dict()

def extract_docs_from_file(filepath: Path, rel_path: Path):
    """Parses a Python file using AST to extract module, class, and function docstrings."""
    try:
        node = ast.parse(filepath.read_text(encoding="utf-8"), filename=str(filepath))
    except (SyntaxError, UnicodeDecodeError):
        return ""

    # Leave this for now, not sure I'll use the module level docstrings or not
    module_name = ".".join(rel_path.with_suffix("").parts)
    mod_doc = ast.get_docstring(node)

    # 2. Walk through top-level elements
    for child in node.body:
        # Classes
        if isinstance(child, ast.ClassDef):
            class_def = DocClass(name=child.name,module_name=module_name)
            class_doc = ast.get_docstring(child)
            if class_doc:
                class_def.set_from_ast(class_doc)

            # Methods inside the class
            for sub_child in child.body:
                if isinstance(sub_child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if sub_child.name.startswith("__init"):
                        args_node = sub_child.args
                        offset = len(args_node.args) - len(args_node.defaults)
                        for i, default_node in enumerate(args_node.defaults):
                            arg_name = args_node.args[offset + i].arg
                            if 'parameters' in classes[child.name] and arg_name in classes[child.name]['parameters']:
                                if isinstance(default_node, ast.Constant):
                                    classes[child.name]['parameters'][arg_name]['default'] = default_node.value
                                else:
                                    classes[child.name]['parameters'][arg_name]['default'] = ast.unparse(default_node)
                    elif not sub_child.name.startswith("_"):
                        if 'methods' not in classes[child.name]:
                            classes[child.name]['methods'] = dict()
                        method_doc = ast.get_docstring(sub_child)
                        method_values = dict()
                        method_values['name'] = sub_child.name
                        if sub_child.returns:
                            return_type_string = ast.unparse(sub_child.returns)
                            method_values['type'] = return_type_string
                        else:
                            method_values['type'] = 'None'
                        if method_doc:
                            method_values['description'] = method_doc
                        else:
                            method_values['description'] = 'Method Not Documented Yet'

                        classes[child.name]['methods'][sub_child.name] = method_values


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
        generate_output()

if __name__ == "__main__":
    generate_docs()

########################################################################################################################
###                                          Data objects                                                            ###
########################################################################################################################

@dataclass
class DocAttribute:
    name: str
    description: str = ""
    type_value: str = ""

    @property
    def title(self):
        return f'[{self.name}](#{self.name})'

    @classmethod
    def from_ast(cls, value:str,class_name:str) -> DocAttribute:
        value = value.replace(":param ", "").strip()
        attribs = value.split(":")
        name = re.search(r'(\w+):', value).group(1)
        type = attribs[0].split(' ')[0]
        if type.startswith("Class"):
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

@dataclass
class DocClass:
    name: str
    module_name: str
    description: str = ""
    doc_attributes: list[DocAttribute] = field(default_factory=list)

    def set_from_ast(self, docstring:str):
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
