#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project: poozos_albatross
@Date: 7/27/26
@File: rossetta

@Author: Phosphor (horuuendillus@gmail.com)
"""
import re
import xml
from collections import namedtuple
from xml.etree.ElementTree import ElementTree
from enum import Enum

from .boreas_rosetta import BoreasRosetta


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Rosetta(metaclass=SingletonMeta):
    doxygen_rosetta: BoreasRosetta

    def __init__(self):
        self.doxygen_rosetta = BoreasRosetta()

    def bbcode_to_rst(self,text:str,underline_is_bold:bool=True,remove_strike_entirely:bool=True)->str:
        # Convert standard tags using regex replacements for reST syntax
        # Bold
        text = re.sub(r'\[b\](.*?)\[/b\]', r'**\1**', text, flags=re.DOTALL)
        # Italic
        text = re.sub(r'\[i\](.*?)\[/i\]', r'*\1*', text, flags=re.DOTALL)
        # Inline code
        text = re.sub(r'\[code\](.*?)\[/code\]', r'``\1``', text, flags=re.DOTALL)
        # Links: [url=url_target]link_text[/url] -> `link_text <url_target>`_
        text = re.sub(r'\[url=(.*?)\](.*?)\[/url\]', r'`\2 <\1>`_', text, flags=re.DOTALL)

        text = re.sub(r'\[br\]', r'\n', text, flags=re.DOTALL)

        if underline_is_bold:
            text = re.sub(r'\[u\](.*?)\[/u\]', r'**\1**', text, flags=re.DOTALL)
        else:
            text = re.sub(r'\[u\](.*?)\[/u\]', r'\1', text, flags=re.DOTALL)

        if remove_strike_entirely:
            text = re.sub(r'\[s\](.*?)\[/s\]', '', text, flags=re.DOTALL)
        else:
            text = re.sub(r'\[s\](.*?)\[/s\]', r'\1', text, flags=re.DOTALL)
        return text