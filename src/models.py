from dataclasses import dataclass

@dataclass
class Question:
    id: int
    question: str
    answer: str
    difficulty: int
    category: str

    def is_correct(self, user_answer: str) -> bool:
        return user_answer.strip().lower() == self.answer.strip().lower()