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
OUTPUT_DIR = script_path.parent.parent / 'docs' / 'argestes'

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
    type_value: str = ""
    args: list[DocArg] = field(default_factory=list)

    @property
    def title(self):
        return self.name

    @classmethod
    def from_ast(cls, ast_def: ast.FunctionDef) ->DocMethod:
        name = ast_def.name
        description = ast.get_docstring(ast_def)
        return_type = "None"
        if description is None:
            description = "Not Documented Yet"
        if ast_def.returns:
            return_type = ast.unparse(ast_def.returns)
        new_doc_method = cls(name=name, description=description, type_value=return_type)
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
                    arg_default = str(default_node.value)
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

    @property
    def has_methods(self) -> bool:
        return len(self.doc_methods) > 0

    @property
    def has_attributes(self) -> bool:
        return len(self.doc_attributes) > 0

    @property
    def is_top_level(self):
        return self.name.startswith(('Class','Description','Brief','Doc'))

    def file_path(self,output_directory:Path) -> Path:
        if self.name.startswith(('Class','Description','Brief')):
            return output_directory / f'{self.name}.md'
        elif self.name.startswith('Doc'):
            return  output_directory / 'custom_lists' / f'{self.name}.md'
        else:
            return output_directory / 'base' / f'{self.name}.md'

    def set_from_docstring(self, docstring:str):
        values = docstring.split("\n")
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

classes : list[DocClass] = []

def make_markdown_table(columns, rows)->str:
    # Create the header row
    header_line = "| " + " | ".join(columns) + " |"
    # Create the separator row
    separator_line = "| " + " | ".join(["---"] * len(columns)) + " |"
    items = []
    for row in rows:
        param = row
        if hasattr(param,'default_value'):
            i = [param.type_value, param.title, param.default_value]
            items.append(i)
        else:
            i = [param.type_value, param.title,""]
            items.append(i)

    body_lines = ["| " + " | ".join(map(str, item)) + " |" for item in items]

    # Combine everything into a single Markdown string
    return "\n".join([header_line, separator_line] + body_lines)


def insert_schema(class_item: DocClass, doc_content):
    if not class_item.is_top_level:
        return
    section_title = '## Schema'
    doc_content.append(f'\n{section_title}\n\n')
    stub_folder = OUTPUT_DIR / 'schema'
    file = next(stub_folder.glob(f'{class_item.name}.xsd_stub'),None)
    if file is not None:
        doc_content.append(f"The following schema definition is derived from Godot's main source repository, and is distributed under the MIT license.\n\n")
        doc_content.append("Attribution: Juan Linietsky, Ariel Manzur and the Godot community\n\n")
        content = file.read_text()
        doc_content.append('```xml\n')
        doc_content.append(f'{content}\n')
        doc_content.append('```')

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
            classes.append(class_def)


def generate_output():
    for class_item in classes:
        doc_content = [f'# {class_item.name}\n']
        if class_item.description:
            doc_content.append(f"\n\n {class_item.description}")
        if class_item.has_attributes:
            section_title = '## Attributes / Parameters:'
            doc_content.append(f'\n\n{section_title}\n')
            attribute_table = make_markdown_table(['Type','Name','Default'],class_item.doc_attributes)
            doc_content.append(f'\n{attribute_table}')
        if class_item.has_methods:
            section_title = '## Methods:'
            doc_content.append(f'\n\n{section_title}\n')
            method_table = make_markdown_table(['Return','Name'],class_item.doc_methods)
            doc_content.append(f'\n{method_table}')
        if class_item.has_attributes:
            section_title = '## Attribute Descriptions:'
            doc_content.append(f'\n\n{section_title}\n')
            for parameter in class_item.doc_attributes:
                section_title = f'\n### {parameter.name}\n'
                doc_content.append(f'{section_title}')
                description = parameter.description
                doc_content.append(f'\n{description}')
        if class_item.has_methods:
            section_title = '## Method Descriptions:'
            doc_content.append(f'\n\n{section_title}\n')
            for method in class_item.doc_methods:
                section_title = f'\n### {method.name}\n'
                doc_content.append(f'{section_title}')
                description = method.description.strip()
                doc_content.append(f'\n{description}')
        insert_schema(class_item,doc_content)
        file = class_item.file_path(OUTPUT_DIR)
        if not file.parent.exists():
            file.parent.mkdir()
        file.write_text("".join(doc_content), encoding="utf-8")


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


