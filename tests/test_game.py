from backend.game import validate_move

START = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


def test_legal_move():
    result = validate_move(START, "e2e4")
    assert result["valid"] is True
    assert result["game_over"] is False


def test_illegal_move():
    assert validate_move(START, "e2e5") == {"valid": False, "error": "illegal move"}


def test_bad_move_format():
    assert validate_move(START, "banana") == {"valid": False, "error": "invalid move format"}


def test_bad_position():
    assert validate_move("not a fen", "e2e4") == {"valid": False, "error": "invalid position"}