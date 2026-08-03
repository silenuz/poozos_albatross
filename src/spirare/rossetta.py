#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 7/27/26
@File: rossetta

@Author: Silenuz Nowan (silenuznowan@yahoo.com)
"""
import re
from enum import Enum

from .boreas_rosetta import BoreasRosetta
from .boreas_rosetta import MarkupElement

class OutputTypes(Enum):
    RST = "rst"

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Rosetta(metaclass=SingletonMeta):
    doxygen_rosetta: BoreasRosetta
    output_markup_map = dict()

    def __init__(self):
        self.doxygen_rosetta = BoreasRosetta()
        self.__init_rst_mappings()

    def __init_rst_mappings(self):
        bold = MarkupElement(open="**", close="**")
        italic = MarkupElement(open="*", close="*")
        code = MarkupElement(open="``", close="``")
        br = MarkupElement(open="\n", close="")
        values = dict()
        values['bold'] = bold
        values['italic'] = italic
        values['code'] = code
        values['br'] = br
        self.output_markup_map[OutputTypes.RST.value] = values


    def bbcode_to_rst(self,text:str,underline_is_bold:bool=True,remove_strike_entirely:bool=True)->str:
       return self._text_to_output_format(text=text,output_format=OutputTypes.RST,
                                          underline_is_bold=underline_is_bold,
                                          remove_strike_entirely=remove_strike_entirely)

    def _text_to_output_format(self,text:str,output_format:OutputTypes,underline_is_bold:bool=True,remove_strike_entirely:bool=True)->str:
        output_elements = self.output_markup_map[output_format.value]

        # Bold
        bold = output_elements['bold']
        text = re.sub(r'\[b\](.*?)\[/b\]', rf'{bold.open}\1{bold.close}', text, flags=re.DOTALL)
        # Italic
        italic = output_elements['italic']
        text = re.sub(r'\[i\](.*?)\[/i\]', rf'{italic.open}\1{italic.close}', text, flags=re.DOTALL)
        # Inline code
        code = output_elements['code']
        text = re.sub(r'\[code\](.*?)\[/code\]', rf'{code.open}\1{code.close}', text, flags=re.DOTALL)
        # Links: todo: figure this out, probably best to do it like the codeblocks specific to each format?
        text = re.sub(r'\[url=(.*?)\](.*?)\[/url\]', r'`\2 <\1>`_', text, flags=re.DOTALL)
        # Linebreaks
        br = output_elements['br']
        text = re.sub(r'\[br\]', rf'{br.open}', text, flags=re.DOTALL)

        # Underline
        if underline_is_bold:
            text = re.sub(r'\[u\](.*?)\[/u\]', rf'{bold.open}\1{bold.close}', text, flags=re.DOTALL)
        else:
            text = re.sub(r'\[u\](.*?)\[/u\]', r'\1', text, flags=re.DOTALL)

        # Strikethrough
        if not 'strike' in output_elements:
            if remove_strike_entirely:
                text = re.sub(r'\[s\](.*?)\[/s\]', '', text, flags=re.DOTALL)
            else:
                text = re.sub(r'\[s\](.*?)\[/s\]', r'\1', text, flags=re.DOTALL)

        return text