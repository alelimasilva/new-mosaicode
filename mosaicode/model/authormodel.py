# -*- coding: utf-8 -*-
"""
This module contains the AuthorModel class.
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class AuthorModel:
    """
    This class contains author information for code generation.
    """

    name: Optional[str] = None
    date: Optional[datetime] = None
    license: Optional[str] = None
