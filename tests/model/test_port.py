# -*- coding: utf-8 -*-
"""
Tests for Port class.
Migrated from unittest to pytest.
"""
import pytest

from mosaicode.model.port import Port


def test_init():
    """Test Port initialization and connection type."""
    model = Port()
    assert model.is_input() is False
    model.conn_type = Port.INPUT
    assert model.is_input() is True
    model.conn_type = Port.OUTPUT
    assert model.is_input() is False

