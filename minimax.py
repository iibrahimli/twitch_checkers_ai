import random
import multiprocessing as mp
from copy import deepcopy
from checkers.game import Game


def static_eval(game: Game) -> int:
    """
    Evaluate a game (player 1 maximizes, player 2 minimizes)

    """

    n_pieces_p = [0, 0]
    for piece in game.board.pieces:
        if piece.captured is False:
            n_pieces_p[piece.player - 1] += 1

    return n_pieces_p[0] - n_pieces_p[1]


def minimax(game: Game, depth: int, minimizing: bool):
    if game.is_over():
        return (12, None) if game.get_winner() == 1 else (-12, None)
    if depth == 0:
        return (static_eval(game), None)
    possible_moves = game.get_possible_moves()
    score = None
    best_move = None
    for move in possible_moves:
        game_copy = deepcopy(game)
        game_copy.move(move)
        mm_score, _ = minimax(game_copy, depth-1, not minimizing)
        if minimizing:
            if score is None or mm_score < score:
                score = mm_score
                best_move = move
        else:
            if score is None or mm_score > score:
                score = mm_score
                best_move = move
    return score, best_move


def play_game(i):
    game = Game()

    print(f"Game {i}")

    while not game.is_over():
        if game.whose_turn() == 1:
            score, move = minimax(game, depth=2, minimizing=False)
            game.move(move)
        else:
            score, move = minimax(game, depth=2, minimizing=True)
            game.move(move)

    return 1 if game.get_winner() == 1 else 0


n_games = 50

pool = mp.Pool(processes=mp.cpu_count() - 3)
res = pool.map(play_game, range(n_games))
mm_wins = sum(res)

print(f"Minimax won {mm_wins}/{n_games} ({mm_wins/n_games*100:.2f}%)")