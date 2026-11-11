import chess


def validate_move(fen: str, uci_move: str) -> dict:
    """Check a move against a position.

    fen: the position as a FEN string.
    uci_move: the move in UCI format, for example "e2e4".
    """
    try:
        board = chess.Board(fen)
    except ValueError:
        return {"valid": False, "error": "invalid position"}

    try:
        move = chess.Move.from_uci(uci_move)
    except ValueError:
        return {"valid": False, "error": "invalid move format"}

    if move not in board.legal_moves:
        return {"valid": False, "error": "illegal move"}

    board.push(move)
    return {"valid": True, "fen": board.fen(), "game_over": board.is_game_over()}