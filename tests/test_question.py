from CodeChallenge.models import Question

import pytest


@pytest.mark.parametrize(
    "guess,answer,match_type,expected",
    [
        ("foo bar", "foo bar", 1, True),
        ("bar foo", "foo bar", 1, False),
        ("name = 'sam'", r"^[a-z_]+ =", 2, True),
        ("name 'sam'", r"^[a-z_]+ =", 2, False),
        (None, "Foo", 1, False),
        (None, r"^[a-z_]+ =", 2, False)
    ]
)
def test_check_correct(guess: str, answer: str, match_type: int, expected: bool):
    question = Question()
    question.answer = answer
    question.match_type = match_type
    assert question.check_correct(guess) is expected