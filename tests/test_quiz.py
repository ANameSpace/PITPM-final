import pytest
from src.quiz import run_quiz
from src.models import Question

def test_run_quiz_empty_list():
    result = run_quiz([], 5, ask_fn=lambda q: "x")
    assert result == {"score": 0, "total": 0, "answers": []}

def test_run_quiz_count_more_than_available():
    questions = [Question(1, "q1", "a", 1, "Math"), Question(2, "q2", "b", 1, "Math")]
    result = run_quiz(questions, 10, ask_fn=lambda q: q.answer)
    assert result["total"] == 2
    assert result["score"] == 2

def test_run_quiz_all_correct():
    questions = [Question(1, "q", "a", 1, "Math")]
    result = run_quiz(questions, 1, ask_fn=lambda q: "a")
    assert result["score"] == 1
    assert result["total"] == 1
    assert result["answers"][0]["correct"] is True

def test_run_quiz_wrong_answer():
    questions = [Question(1, "q", "a", 1, "Math")]
    result = run_quiz(questions, 1, ask_fn=lambda q: "wrong")
    assert result["score"] == 0

def test_run_quiz_mixed():
    questions = [
        Question(1, "q1", "a", 1, "Math"),
        Question(2, "q2", "b", 1, "Math"),
    ]
    answers = iter(["a", "wrong"])
    result = run_quiz(questions, 2, ask_fn=lambda q: next(answers))
    # Из-за random.sample порядок может меняться, проверяем структуру
    assert result["total"] == 2
    assert 0 <= result["score"] <= 2
    assert len(result["answers"]) == 2