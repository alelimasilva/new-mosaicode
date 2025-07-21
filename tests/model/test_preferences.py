# -*- coding: utf-8 -*-
"""
Tests for Preferences class.
Migrated from unittest to pytest.
"""
import pytest

from mosaicode.model.preferences import Preferences


def test_init():
    """Test Preferences initialization."""
    model = Preferences()
    assert model is not None

