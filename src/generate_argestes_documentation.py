#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 7/2/26
@File: gen_docs

@Author: Phosphor (horuuendillus@gmail.com)
"""
import ast
import os
import re
from pathlib import Path

# Get the absolute path to this script
script_path = Path(__file__).resolve()
PACKAGE_DIR = script_path.parent / 'spirare' / 'argestes'
OUTPUT_DIR = script_path.parent / 'docs' / 'argestes'
classes = dict()


def process_class_definition(class_name: str, docstring: str):
    values = docstring.split("\n")
    output: list[str] = []
    for value in values:
        print("Value:: " + value)
        if value.startswith(':param'):
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
            new_value = f'* Parameter: **{name}** \n\t- Type: {type_value} \n\t- Description: {description}'
            output.append(new_value)
            if not 'parameters' in classes[class_name]:
                classes[class_name]['parameters'] = dict()
            parameter_values = dict()
            parameter_values['name'] = name
            parameter_values['description'] = description
            parameter_values['type'] = type_value
            classes[class_name]['parameters'][name] = parameter_values
        else:
            print("Is Description")
            if not 'description' in classes[class_name]:
                classes[class_name]['description'] = value
            else:
                classes[class_name]['description'] += ' ' + value


def extract_docs_from_file(filepath: Path, rel_path: Path):
    """Parses a Python file using AST to extract module, class, and function docstrings."""
    try:
        node = ast.parse(filepath.read_text(encoding="utf-8"), filename=str(filepath))
    except (SyntaxError, UnicodeDecodeError):
        return ""

    # Convert path to python module dot-notation (e.g., package.submodule)
    module_name = ".".join(rel_path.with_suffix("").parts)
    md: str = ''

    # 1. Module Docstring
    mod_doc = ast.get_docstring(node)
    md = (f"# Module: `{module_name}`\n\n")
    if mod_doc:
        content = mod_doc.strip().replace("@Author: Silenuz Nowan (silenuznowan@yahoo.com)", "")
        md = md + (f"{content}\n\n")

    # 2. Walk through top-level elements
    for child in node.body:
        # Classes
        if isinstance(child, ast.ClassDef):
            class_def = []
            class_doc = ast.get_docstring(child)
            class_def.append(f"## 📦 Class: `{child.name}`\n\n")
            classes[child.name] = dict()

            if class_doc:
                process_class_definition(child.name, class_doc)

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
                            classes[child.name]['methods'] = []
                        method_doc = ast.get_docstring(sub_child)
                        method_values = dict()
                        method_values['name'] = sub_child.name
                        if method_doc:
                            method_values['description'] = method_doc
                        classes[child.name]['methods'].append(method_values)


def make_markdown_table(columns, rows)->str:
    # Create the header row
    header_line = "| " + " | ".join(columns) + " |"
    # Create the separator row
    separator_line = "| " + " | ".join(["---"] * len(columns)) + " |"
    items = []
    for row in rows:
        param = rows[row]
        if 'default' in param:
            i = [param['type'], param['name'], param['default']]
            items.append(i)
        else:
            i = [param['type'], param['name'],""]
            items.append(i)

    body_lines = ["| " + " | ".join(map(str, item)) + " |" for item in items]

    # Combine everything into a single Markdown string
    return "\n".join([header_line, separator_line] + body_lines)


def generate_output():
    for class_item in classes:
        doc_content = []
        class_doc = classes[class_item]
        doc_content.append(f'{class_item}\n' )
        doc_content.append('=' * len(class_item))
        if 'description' in class_doc:
            doc_content.append(f"\n\n {class_doc['description']}")
        if 'parameters' in class_doc:
            section_title = 'Attributes / Parameters:'
            doc_content.append(f'\n\n{section_title}\n')
            doc_content.append('-' * len(section_title))
            attribute_table = make_markdown_table(['Type','Name','Default'],class_doc['parameters'])
            doc_content.append(f'\n{attribute_table}')
        print("".join(doc_content))

def generate_docs():
    pkg_path = PACKAGE_DIR

    if not pkg_path.exists():
        print(f"Error: Folder '{PACKAGE_DIR}' not found.")
        return

    generated_files = 0

    for file_path in pkg_path.rglob("*.py"):
        if file_path.name.startswith("_"):
            continue

        # Get path relative to the parent of the package directory
        rel_path = file_path.relative_to(pkg_path.parent)
        extract_docs_from_file(file_path, rel_path)
        generate_output()
    print(f"Done! Created {generated_files} Markdown files inside the '{OUTPUT_DIR}/' folder.")
    print(classes)


if __name__ == "__main__":
    generate_docs()