import csv
from pathlib import Path
from .models import Question

DEFAULT_PATH = Path("data/questions.csv")
HEADERS = ["id", "question", "answer", "difficulty", "category"]

def ensure_file(path: Path = DEFAULT_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        with path.open("w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(HEADERS)

def read_all(path: Path = DEFAULT_PATH) -> list[Question]:
    ensure_file(path)
    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [
            Question(
                id=int(r["id"]),
                question=r["question"],
                answer=r["answer"],
                difficulty=int(r["difficulty"]),
                category=r["category"],
            )
            for r in reader
        ]

def _next_id(questions: list[Question]) -> int:
    return max((q.id for q in questions), default=0) + 1

def save(question: Question, path: Path = DEFAULT_PATH) -> Question:
    ensure_file(path)
    questions = read_all(path)
    if question.id == 0:
        new_id = _next_id(questions)
        new_q = Question(new_id, question.question, question.answer,
                         question.difficulty, question.category)
        questions.append(new_q)
    else:
        new_q = question
        for i, q in enumerate(questions):
            if q.id == question.id:
                questions[i] = new_q
                break
    _write_all(questions, path)
    return new_q

def delete(qid: int, path: Path = DEFAULT_PATH) -> bool:
    ensure_file(path)
    questions = read_all(path)
    filtered = [q for q in questions if q.id != qid]
    if len(filtered) == len(questions):
        return False
    _write_all(filtered, path)
    return True

def _write_all(questions: list[Question], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEADERS)
        w.writeheader()
        for q in questions:
            w.writerow({
                "id": q.id,
                "question": q.question,
                "answer": q.answer,
                "difficulty": q.difficulty,
                "category": q.category,
            })

def filter_by(questions: list[Question], *, category=None,
              min_diff=None, max_diff=None) -> list[Question]:
    result = questions
    if category is not None:
        result = [q for q in result if q.category == category]
    if min_diff is not None:
        result = [q for q in result if q.difficulty >= min_diff]
    if max_diff is not None:
        result = [q for q in result if q.difficulty <= max_diff]
    return result