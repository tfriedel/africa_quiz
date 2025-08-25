from africa_quiz import hello


def test_hello() -> None:
    result = hello()
    expected = "Hello from africa_quiz!"
    assert result == expected


def test_hello_return_type() -> None:
    result = hello()
    assert isinstance(result, str)
