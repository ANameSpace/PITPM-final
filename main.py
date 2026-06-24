import sys
from src.models import Question
from src.storage import read_all, save, delete, filter_by
from src.quiz import run_quiz

def input_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Введите целое число.")

def input_difficulty(prompt: str) -> int:
    """Запрос сложности с валидацией диапазона 1-5."""
    while True:
        try:
            value = int(input(prompt))
            if 1 <= value <= 5:
                return value
            print("Сложность должна быть от 1 до 5.")
        except ValueError:
            print("Введите целое число.")

def input_nonempty(prompt: str) -> str:
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print("Поле не может быть пустым.")

def add_question():
    q_text = input_nonempty("Вопрос: ")
    a_text = input_nonempty("Ответ: ")
    diff = input_difficulty("Сложность (1-5): ")
    cat = input_nonempty("Категория: ")
    q = Question(0, q_text, a_text, diff, cat)
    saved = save(q)
    print(f"Сохранено с id={saved.id}")

def list_questions():
    items = read_all()
    if not items:
        print("Вопросов пока нет.")
        return
    for q in items:
        print(f"[{q.id}] {q.category} (сложн. {q.difficulty}) — {q.question}")

def delete_question():
    qid = input_int("ID для удаления: ")
    if delete(qid):
        print("Удалено.")
    else:
        print(f"Вопрос с id={qid} не найден.")

def filter_questions():
    cat = input("Категория (пусто — все): ").strip() or None
    min_d = input("Мин. сложность (пусто — нет): ").strip()
    max_d = input("Макс. сложность (пусто — нет): ").strip()
    result = filter_by(
        read_all(),
        category=cat,
        min_diff=int(min_d) if min_d else None,
        max_diff=int(max_d) if max_d else None,
    )
    for q in result:
        print(f"[{q.id}] {q.question}")

def start_quiz():
    items = read_all()
    if not items:
        print("Нет вопросов. Добавьте хотя бы один.")
        return
    count = input_int(f"Сколько вопросов? (1-{len(items)}): ")
    count = min(max(1, count), len(items))
    result = run_quiz(items, count, ask_fn=lambda q: input(f"{q.question}\n> "))
    print(f"\nРезультат: {result['score']} из {result['total']}")

def menu():
    actions = {
        "1": add_question,
        "2": list_questions,
        "3": delete_question,
        "4": filter_questions,
        "5": start_quiz,
    }
    while True:
        print("\nQuizA")
        print("1. Добавить вопрос")
        print("2. Список вопросов")
        print("3. Удалить вопрос")
        print("4. Фильтр")
        print("5. Викторина")
        print("0. Выход")
        choice = input("> ").strip()
        if choice == "0":
            break
        if choice in actions:
            try:
                actions[choice]()
            except KeyboardInterrupt:
                print("\nОтменено.")
        else:
            print("Неизвестный пункт.")

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\nДо свидания!")
        sys.exit(0)