import pytest
from src.models import Question

def test_question_creation():
    q = Question(1, "2+2?", "4", 1, "Math")
    assert q.id == 1
    assert q.question == "2+2?"

def test_is_correct_case_insensitive():
    q = Question(1, "Capital of France?", "Paris", 1, "Geo")
    assert q.is_correct("paris") is True
    assert q.is_correct("PARIS") is True
    assert q.is_correct("  Paris  ") is True
    assert q.is_correct("London") is False

def test_is_correct_empty():
    q = Question(1, "?", "", 1, "Misc")
    assert q.is_correct("") is True
    assert q.is_correct("no") is False