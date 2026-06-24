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