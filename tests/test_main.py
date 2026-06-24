import main


def test_input_difficulty_rejects_too_high(monkeypatch):
    """Сложность больше 5 должна отклоняться"""
    inputs = iter(["99", "-5", "0", "6", "3"])  # невалидные, потом валидное

    def mock_input(prompt):
        return next(inputs)

    monkeypatch.setattr("builtins.input", mock_input)

    result = main.input_difficulty("Сложность (1-5): ")
    assert result == 3  # принято только валидное значение


def test_input_difficulty_accepts_valid_range(monkeypatch):
    """Все значения от 1 до 5 принимаются"""
    for valid in [1, 2, 3, 4, 5]:
        monkeypatch.setattr("builtins.input", lambda p: str(valid))
        assert main.input_difficulty("Сложность (1-5): ") == valid

def test_show_statistics_empty(capsys, monkeypatch):
    monkeypatch.setattr("main.read_all", lambda: [])
    main.show_statistics()
    assert "Вопросов пока нет" in capsys.readouterr().out


def test_show_statistics_with_data(capsys, monkeypatch):
    from src.models import Question
    questions = [
        Question(1, "q1", "a1", 1, "Math"),
        Question(2, "q2", "a2", 3, "Math"),
        Question(3, "q3", "a3", 2, "Geo"),
    ]
    monkeypatch.setattr("main.read_all", lambda: questions)
    main.show_statistics()
    out = capsys.readouterr().out
    assert "Всего вопросов: 3" in out
    assert "Math: 2" in out
    assert "Geo: 1" in out
    assert "Средняя сложность: 2.0" in out