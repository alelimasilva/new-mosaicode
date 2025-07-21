# -*- coding: utf-8 -*-
"""
Tests for Persistence class.
Migrated from unittest to pytest.
"""
import os
import pytest

from mosaicode.utils.FileUtils import *
from mosaicode.persistence.persistence import Persistence


def test_create_dir():
    """Test Persistence.create_dir method."""
    Persistence.create_dir(None)
    Persistence.create_dir("/etc/")
    Persistence.create_dir("/tmp/test")
    os.rmdir("/tmp/test")

