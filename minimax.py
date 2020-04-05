import random
import multiprocessing as mp
from copy import deepcopy
from tqdm import tqdm
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


def minimax(game, depth, minimizing, alpha=float('-inf'), beta=float('inf')):
    if game.is_over():
        winner = game.get_winner()
        if winner == 1:
            return (12, None)
        elif winner == 2:
            return (-12, None)
        else:
            return (0, None)
    if depth == 0:
        return (static_eval(game), None)
    possible_moves = game.get_possible_moves()
    score = None
    best_move = None
    for move in possible_moves:
        game_copy = deepcopy(game)
        game_copy.move(move)
        mm_score, _ = minimax(game_copy, depth-1, not minimizing, alpha, beta)
        if minimizing:
            if score is None or mm_score < score:
                score = mm_score
                best_move = move
                alpha = max(alpha, score)
                if alpha >= beta:
                    break
        else:
            if score is None or mm_score > score:
                score = mm_score
                best_move = move
                beta = min(beta, score)
                if alpha >= beta:
                    break
    return score, best_move


def play_game(i):
    game = Game()

    # print(f"Game {i}")

    while not game.is_over():
        if game.whose_turn() == 1:
            score, move = minimax(game, depth=4, minimizing=False)
            game.move(move)
        else:
            game.move(random.choice(game.get_possible_moves()))
            # score, move = minimax(game, depth=2, minimizing=True)
            # game.move(move)

    winner = game.get_winner()
    if winner == 1:
        return 1
    elif winner == 2:
        return -1
    else:
        return 0


n_games = 100

first_wins  = 0
second_wins = 0
draws       = 0
pool = mp.Pool(processes=mp.cpu_count() - 3)

with mp.Pool(processes=mp.cpu_count() - 3) as pool:
    with tqdm(total=n_games) as pbar:
        for _, res in enumerate(pool.imap_unordered(play_game, range(n_games))):
            if res == 1:
                first_wins += 1
            elif res == -1:
                second_wins += 1
            else:
                draws += 1
            pbar.update()

print(f"First player:  {first_wins:4}/{n_games} ({first_wins/n_games*100:.2f}%)")
print(f"Second player: {second_wins:4}/{n_games} ({second_wins/n_games*100:.2f}%)")
print(f"Draws:         {draws:4}/{n_games} ({draws/n_games*100:.2f}%)")
