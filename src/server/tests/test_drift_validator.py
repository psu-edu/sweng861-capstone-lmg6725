from services.drift_validator import validate_response


def test_valid_response_returns_true():
    data = {"choices": [{"message": "hello"}]}
    assert validate_response(data) is True


def test_missing_choices_returns_false():
    data = {}
    assert validate_response(data) is False


def test_empty_choices_returns_false():
    data = {"choices": []}
    assert validate_response(data) is False