from app.tools.calculator import calculate


def test_calculator_basic_expression():
    assert calculate("10 + 5 * 2") == "20"
