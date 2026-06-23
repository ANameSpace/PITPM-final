import pytest
from pathlib import Path
from src.storage import (
    save, read_all, delete, filter_by, ensure_file, _next_id
)
from src.models import Question

@pytest.fixture
def tmp_csv(tmp_path, monkeypatch):
    p = tmp_path / "questions.csv"
    monkeypatch.setattr("src.storage.DEFAULT_PATH", p)
    ensure_file(p)
    return p

def test_ensure_file_creates_csv(tmp_path, monkeypatch):
    p = tmp_path / "new.csv"
    monkeypatch.setattr("src.storage.DEFAULT_PATH", p)
    ensure_file(p)
    assert p.exists()

def test_read_empty_returns_empty_list(tmp_csv):
    assert read_all(tmp_csv) == []

def test_save_assigns_id(tmp_csv):
    q = Question(0, "2+2?", "4", 1, "Math")
    saved = save(q, tmp_csv)
    assert saved.id == 1

def test_save_multiple_increment_ids(tmp_csv):
    save(Question(0, "q1", "a1", 1, "Math"), tmp_csv)
    save(Question(0, "q2", "a2", 2, "Geo"), tmp_csv)
    items = read_all(tmp_csv)
    assert [q.id for q in items] == [1, 2]

def test_save_updates_existing(tmp_csv):
    q = save(Question(0, "old", "a", 1, "Math"), tmp_csv)
    updated = save(Question(q.id, "new", "b", 2, "Geo"), tmp_csv)
    items = read_all(tmp_csv)
    assert len(items) == 1
    assert items[0].question == "new"

def test_delete_existing(tmp_csv):
    q = save(Question(0, "q", "a", 1, "Math"), tmp_csv)
    assert delete(q.id, tmp_csv) is True
    assert read_all(tmp_csv) == []

def test_delete_missing_returns_false(tmp_csv):
    assert delete(999, tmp_csv) is False

def test_question_with_commas(tmp_csv):
    q = save(Question(0, "Who said 'Hello, world'?", "X", 1, "Misc"), tmp_csv)
    items = read_all(tmp_csv)
    assert items[0].question == "Who said 'Hello, world'?"

def test_filter_by_category(tmp_csv):
    save(Question(0, "q1", "a", 1, "Math"), tmp_csv)
    save(Question(0, "q2", "a", 1, "Geo"), tmp_csv)
    result = filter_by(read_all(tmp_csv), category="Math")
    assert len(result) == 1
    assert result[0].category == "Math"

def test_filter_by_difficulty(tmp_csv):
    save(Question(0, "q1", "a", 1, "Math"), tmp_csv)
    save(Question(0, "q2", "a", 3, "Math"), tmp_csv)
    save(Question(0, "q3", "a", 5, "Math"), tmp_csv)
    result = filter_by(read_all(tmp_csv), min_diff=2, max_diff=4)
    assert len(result) == 1