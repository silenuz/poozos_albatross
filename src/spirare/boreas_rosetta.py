#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 7/28/26
@File: boreas_rosetta

@Author: Silenuz Nowan (silenuznowan@yahoo.com)
"""
import re
import xml
from collections import namedtuple
from xml.etree.ElementTree import ElementTree
from enum import Enum

MarkupElement = namedtuple('MarkupElement',['open','close'])

class DoxygenOutputTypes(Enum):
    BBCode = "bbcode"

class BoreasRosetta:

    output_markup_map = dict()

    # track xml tags that should not be parsed, such as htmlonly
    element_black_list_set = set()
    element_black_list_set.add("htmlonly")
    element_black_list_set.add("manonly")
    element_black_list_set.add("latexonly")
    element_black_list_set.add("xrefsect")

    def __init__(self):
        self.output_markup_map[DoxygenOutputTypes.BBCode] = self.__create_bbcode_format_map()
        
    def __create_bbcode_format_map(self)->dict:
        values = dict()
        values['bold'] = MarkupElement(open="[b]", close=r"[/b]")
        values['italic'] = MarkupElement(open="[i]", close=r"[/i]")
        values['underline'] = MarkupElement(open="[u]", close=r"[/u]")
        values['strikethrough'] = MarkupElement(open="[s]", close=r"[/s]")
        values['code'] = MarkupElement(open="[code]", close=r"[/code]")
        values['keyboard'] = MarkupElement(open="[kbd]", close=r"[/kbd]")
        values['linebreak'] = MarkupElement(open="[br]", close=r"")
        values['link'] = MarkupElement(open="[url]", close=r"[/url]")
        return values

    def doxygen_to_bbcode(self, element: str | xml.etree.ElementTree.Element):
        if isinstance(element, str):
            element = xml.etree.ElementTree.fromstring(f'<myelement>{element}</myelement>')
        return self.get_tag_text(element, DoxygenOutputTypes.BBCode)


    def get_tag_text(self, element: xml.etree.ElementTree.Element, output_format: DoxygenOutputTypes = DoxygenOutputTypes.BBCode):
        #print("getting tag text")
        format_map = self.output_markup_map[output_format]
        parts = []
        if element.text:
            parts.append(element.text.strip())
        para_nodes = element.findall('para')
        count = len(para_nodes)
        #print("count")
        for paragraph_index in range(count):
            paragraph = para_nodes[paragraph_index]
            empty_element = True
            element_text = self.parse_xml_text(paragraph,format_map)
            if element_text:
                parts.append(element_text)
                empty_element = False
            if not empty_element and paragraph_index != count - 1:
                parts.append(format_map['linebreak'].open)
                parts.append(format_map['linebreak'].open)

        text = " ".join(parts)

        return text

    def parse_xml_text(self, element: xml.etree.ElementTree.Element, format_map: dict) -> str:
        #print("Parsing xml text")
        parts = []
        has_existing_codeblock = False

        if element.tag in self.element_black_list_set:
            return ""

        if element.tag == 'para':
            if len(element) > 0:
                if element[0].tag == 'xrefsect':
                    return ""

        if element.text is not None:
            parts.append(element.text.strip())

        for mixed_element_node in element:
            if mixed_element_node.tag in format_map:
                markup = format_map[mixed_element_node.tag]
                if not mixed_element_node.text is None:
                    content = markup.open + mixed_element_node.text.strip()
                else:
                    content = markup.open
                parts.append(content)
                if len(mixed_element_node):
                    child_content = self.parse_xml_text(mixed_element_node,format_map)
                    parts[-1] = parts[-1] + child_content.strip()
                parts[-1] = parts[-1] + markup.close
            elif mixed_element_node.tag == "godotonly" and mixed_element_node.get("kind") == 'text':

                if mixed_element_node.tail is not None:
                    node_tail = mixed_element_node.tail.rstrip()
                else:
                    node_tail = ""
                if mixed_element_node.get("content") is not None:
                    content = mixed_element_node.get("content")
                else:
                    content = ""

                if mixed_element_node.get('position') == "close":
                    parts[-1] = parts[-1] + content + node_tail
                else:
                    parts.append(content + node_tail)
            elif mixed_element_node.tag == "programlisting":
                # todo: fix code block generation so that proper indentation is preserved
                insert_index = len(parts) - 1
                existing_is_godot = True
                if has_existing_codeblock:
                    insert_index = next(i for i, s in enumerate(parts) if s.startswith('[codeblock'))
                    current_codeblock = parts[insert_index]
                    lang_pattern = r'lang=(.*?)\]'
                    lang_value = re.search(lang_pattern, current_codeblock).group(1)
                    current_codeblock = current_codeblock.replace('codeblock lang=', '')
                    current_codeblock = current_codeblock.replace('/codeblock', f'/{lang_value}')
                    parts[insert_index] = current_codeblock
                    if lang_value == 'csharp':
                        existing_is_godot = False

                file_extension = mixed_element_node.get("filename").replace('.', '')
                if file_extension == 'cs':
                    language = 'csharp'
                else:
                    language = file_extension

                block_text = []
                line_nodes = mixed_element_node.findall('codeline')
                for line_node in line_nodes:
                    line = " ".join(line_node.itertext()) + "\n"
                    block_text.append(line)

                if has_existing_codeblock:
                    if existing_is_godot:
                        parts[insert_index] = '[codeblocks]' + parts[insert_index]
                        parts[insert_index] = f'[{language}]]' + "".join(block_text) + f'[/{language}]'
                        parts[insert_index] = parts[insert_index] + '[/codeblocks]'
                    else:
                        current_block = parts[insert_index]
                        parts[insert_index] = f'[codeblocks][{language}]' + "".join(block_text) + f'[/{language}]'
                        parts[insert_index] = parts[insert_index] + current_block + '[/codeblocks]'
                else:
                    parts.append(f'[codeblock lang={language}]' + "".join(block_text) + f'[/codeblock]')

                has_existing_codeblock = True
            else:
                if not mixed_element_node.text is None:
                    parts.append(" ".join(mixed_element_node.itertext()))

            if not mixed_element_node.tail is None and not mixed_element_node.tail == " ":
                if not mixed_element_node.tag == "godotonly":
                    parts.append(mixed_element_node.tail.strip())

        text = " ".join(parts)
        return text