# -*- coding: utf-8 -*-
"""
Tests for CommentModel class.
Migrated from unittest/TestBase to pytest.
"""
import pytest
from mosaicode.GUI.fieldtypes import * 
from mosaicode.model.commentmodel import CommentModel

@pytest.fixture
def comment():
    return CommentModel()

def test_commentmodel_new(comment):
    comment.set_properties({"text": "Novo Teste"})
    comment.set_properties({"Not here": "Novo Teste"})
    str(comment)

    comment.set_properties(None)
    str(comment)

    comment.properties = []
    str(comment)

    comment.properties = []
    str(comment)

    comment.properties = []
    comment.set_properties({"text": "Novo Teste"})
    str(comment)

    comment.properties = [{"test": "Test"}]
    str(comment)

    comment = CommentModel()

