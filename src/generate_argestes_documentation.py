#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 7/2/26
@File: gen_docs

@Author: Silenuz Nowan (silenuznowan@yahoo.com)

“Life is full of questions. Idiots are full of answers.”

todo: this script has become a mess.  If i'm going to include I should at least make it a little less Ugly
"""
import ast
import re
from pathlib import Path


# Get the absolute path to this script
script_path = Path(__file__).resolve()
PACKAGE_DIR = script_path.parent / 'spirare' / 'argestes'
OUTPUT_DIR = script_path.parent.parent / 'docs' / 'argestes'
BASE_DIRECTORY = OUTPUT_DIR / 'base'
LIST_DIRECTORY = OUTPUT_DIR / 'custom_lists'
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
            parameter_values['name'] = f'[{name}](#{name})'
            parameter_values['title'] = name
            parameter_values['description'] = description
            parameter_values['type'] = type_value
            classes[class_name]['parameters'][name] = parameter_values
        else:
            print("Is Description")
            if not 'description' in classes[class_name]:
                classes[class_name]['description'] = value
            else:
                classes[class_name]['description'] += '\n' + value


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
        has_params = False
        has_methods = False

        if 'description' in class_doc:
            doc_content.append(f"\n\n {class_doc['description']}")
        if 'parameters' in class_doc:
            has_params = True
            section_title = '## Attributes / Parameters:'
            doc_content.append(f'\n\n{section_title}\n')
            attribute_table = make_markdown_table(['Type','Name','Default'],class_doc['parameters'])
            doc_content.append(f'\n{attribute_table}')
        if 'methods' in class_doc:
            has_methods = True
            section_title = '## Methods:'
            doc_content.append(f'\n\n{section_title}\n')
            method_table = make_markdown_table(['Return','Name'],class_doc['methods'])
            doc_content.append(f'\n{method_table}')
        if has_params:
            section_title = '## Attribute Descriptions:'
            doc_content.append(f'\n\n{section_title}\n')
            for param in class_doc['parameters']:
                parameter = class_doc['parameters'][param]
                section_title = f'\n### {parameter['title']}\n'
                print("Title: " , section_title)
                doc_content.append(f'{section_title}')
                description = parameter['description'].strip()
                print("Description: ",description)
                doc_content.append(f'\n{description}')
                print("\n".join(doc_content))
        if has_methods:
            section_title = '## Method Descriptions:'
            doc_content.append(f'\n\n{section_title}\n')
            for meth in class_doc['methods']:
                method = class_doc['methods'][meth]
                section_title = f'\n### {method['name']}\n'
                print("Title: " , section_title)
                doc_content.append(f'{section_title}')
                description = method['description'].strip()
                print("Description: ",description)
                doc_content.append(f'\n{description}')
                print("\n".join(doc_content))

        if class_item.startswith('Class'):
            file = OUTPUT_DIR / f'{class_item}.md'
        elif class_item.startswith('Doc'):
            file = LIST_DIRECTORY / f'{class_item}.md'
        else:
            file = BASE_DIRECTORY / f'{class_item}.md'

        file.write_text("".join(doc_content), encoding="utf-8")

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