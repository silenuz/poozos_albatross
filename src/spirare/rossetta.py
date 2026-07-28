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