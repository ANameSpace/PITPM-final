import random
from .models import Question

def run_quiz(questions: list[Question], count: int, ask_fn=None) -> dict:
    if not questions:
        return {"score": 0, "total": 0, "answers": []}
    pool = random.sample(questions, min(count, len(questions)))
    answers = []
    for q in pool:
        user = ask_fn(q) if ask_fn else ""
        answers.append({
            "question": q.question,
            "user_answer": user,
            "correct": q.is_correct(user),
        })
    return {
        "score": sum(1 for a in answers if a["correct"]),
        "total": len(answers),
        "answers": answers,
    }