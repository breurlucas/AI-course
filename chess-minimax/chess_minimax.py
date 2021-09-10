# Beatriz Paiva & Lucas Breur
# Senac 2021 - Artificial Intelligence course

import chess
import random

class Bot:

    board = chess.Board()

    def select_play(self):
        return random.choice([play for play in self.board.legal_moves])