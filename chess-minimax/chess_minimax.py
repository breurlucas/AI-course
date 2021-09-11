# Beatriz Paiva & Lucas Breur
# Senac 2021 - Artificial Intelligence course

import chess

MAX_DEPTH = 3

class Bot:

    board = chess.Board()

    # https://www.chessprogramming.org/Simplified_Evaluation_Function
    # Evalutation heuristic based on piece value and piece-square tables

    # The code below from Andreas Stöckl implements these heuristics
    # https://andreasstckl.medium.com/writing-a-chess-program-in-one-day-30daff4610ec
        
    # START

    def evaluate_state(self):

        # Check if any of the four final states has been reached

        # If one of the players won, check which one
        if self.board.is_checkmate():
            if self.board.turn:
                return -10000 # The player won
            else:
                return 10000 # The bot won

        # Draw
        if self.board.is_stalemate():
                return 0
        if self.board.is_insufficient_material():
                return 0

        # Define values for each piece type
        pawn_v = 100
        rook_v = 320
        bish_v = 330
        knig_v = 500
        quee_v = 900

        # Assign values and subtract black from white
        pawn_eval = pawn_v*(len(self.board.pieces(chess.PAWN, chess.WHITE)) - len(self.board.pieces(chess.PAWN, chess.BLACK)))
        rook_eval = rook_v*(len(self.board.pieces(chess.ROOK, chess.WHITE)) - len(self.board.pieces(chess.ROOK, chess.BLACK)))
        bish_eval = bish_v*(len(self.board.pieces(chess.BISHOP, chess.WHITE)) - len(self.board.pieces(chess.BISHOP, chess.BLACK)))
        knig_eval = knig_v*(len(self.board.pieces(chess.KNIGHT, chess.WHITE)) - len(self.board.pieces(chess.KNIGHT, chess.BLACK)))
        quee_eval = quee_v*(len(self.board.pieces(chess.QUEEN, chess.WHITE)) - len(self.board.pieces(chess.QUEEN, chess.BLACK)))

        piece_eval = pawn_eval + rook_eval + bish_eval + knig_eval + quee_eval
        
        pawntable = [
        0,  0,  0,  0,  0,  0,  0,  0,
        5, 10, 10,-20,-20, 10, 10,  5,
        5, -5,-10,  0,  0,-10, -5,  5,
        0,  0,  0, 20, 20,  0,  0,  0,
        5,  5, 10, 25, 25, 10,  5,  5,
        10, 10, 20, 30, 30, 20, 10, 10,
        50, 50, 50, 50, 50, 50, 50, 50,
        0,  0,  0,  0,  0,  0,  0,  0]

        knightstable = [
        -50,-40,-30,-30,-30,-30,-40,-50,
        -40,-20,  0,  5,  5,  0,-20,-40,
        -30,  5, 10, 15, 15, 10,  5,-30,
        -30,  0, 15, 20, 20, 15,  0,-30,
        -30,  5, 15, 20, 20, 15,  5,-30,
        -30,  0, 10, 15, 15, 10,  0,-30,
        -40,-20,  0,  0,  0,  0,-20,-40,
        -50,-40,-30,-30,-30,-30,-40,-50]

        bishopstable = [
        -20,-10,-10,-10,-10,-10,-10,-20,
        -10,  5,  0,  0,  0,  0,  5,-10,
        -10, 10, 10, 10, 10, 10, 10,-10,
        -10,  0, 10, 10, 10, 10,  0,-10,
        -10,  5,  5, 10, 10,  5,  5,-10,
        -10,  0,  5, 10, 10,  5,  0,-10,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -20,-10,-10,-10,-10,-10,-10,-20]

        rookstable = [
        0,  0,  0,  5,  5,  0,  0,  0,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        5, 10, 10, 10, 10, 10, 10,  5,
        0,  0,  0,  0,  0,  0,  0,  0]

        queenstable = [
        -20,-10,-10, -5, -5,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  5,  5,  5,  5,  5,  0,-10,
        0,  0,  5,  5,  5,  5,  0, -5,
        -5,  0,  5,  5,  5,  5,  0, -5,
        -10,  0,  5,  5,  5,  5,  0,-10,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -20,-10,-10, -5, -5,-10,-10,-20]

        kingstable = [
        20, 30, 10,  0,  0, 10, 30, 20,
        20, 20,  0,  0,  0,  0, 20, 20,
        -10,-20,-20,-20,-20,-20,-20,-10,
        -20,-30,-30,-40,-40,-30,-30,-20,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30]

        pawnsq = sum([pawntable[i] for i in self.board.pieces(chess.PAWN, chess.WHITE)])
        pawnsq= pawnsq + sum([-pawntable[chess.square_mirror(i)] 
                                        for i in self.board.pieces(chess.PAWN, chess.BLACK)])
        knightsq = sum([knightstable[i] for i in self.board.pieces(chess.KNIGHT, chess.WHITE)])
        knightsq = knightsq + sum([-knightstable[chess.square_mirror(i)] 
                                        for i in self.board.pieces(chess.KNIGHT, chess.BLACK)])
        bishopsq= sum([bishopstable[i] for i in self.board.pieces(chess.BISHOP, chess.WHITE)])
        bishopsq= bishopsq + sum([-bishopstable[chess.square_mirror(i)] 
                                        for i in self.board.pieces(chess.BISHOP, chess.BLACK)])
        rooksq = sum([rookstable[i] for i in self.board.pieces(chess.ROOK, chess.WHITE)]) 
        rooksq = rooksq + sum([-rookstable[chess.square_mirror(i)] 
                                        for i in self.board.pieces(chess.ROOK, chess.BLACK)])
        queensq = sum([queenstable[i] for i in self.board.pieces(chess.QUEEN, chess.WHITE)]) 
        queensq = queensq + sum([-queenstable[chess.square_mirror(i)] 
                                        for i in self.board.pieces(chess.QUEEN, chess.BLACK)])
        kingsq = sum([kingstable[i] for i in self.board.pieces(chess.KING, chess.WHITE)]) 
        kingsq = kingsq + sum([-kingstable[chess.square_mirror(i)] 
                                        for i in self.board.pieces(chess.KING, chess.BLACK)])
        
        evaluation = piece_eval + pawnsq + knightsq + bishopsq+ rooksq+ queensq + kingsq

        # Verifies whose turn it is and returns the evaluation accordingly
        if self.board.turn:
            return evaluation
        else:
            return -evaluation
    
    # END
    
    def minimax_alfabeta(self, depth = MAX_DEPTH, alfa = -100000, beta = 100000):
        
        if self.board.is_checkmate() or self.board.is_stalemate() or self.board.is_insufficient_material() or depth == 0:
            return self.evaluate_state()

        if self.board.turn: # Bot's turn
            for play in self.board.legal_moves:
                self.board.push(play)
                evaluation = self.minimax_alfabeta(depth - 1, alfa, beta)
                alfa = max(evaluation, alfa)

                if beta <= alfa:
                    break

                self.board.pop()

                return alfa

        else: # Player's turn
            for play in self.board.legal_moves:
                self.board.push(play)
                evaluation = self.minimax_alfabeta(depth - 1, alfa, beta)
                beta = min(evaluation, beta)

                if beta <= alfa:
                    break
                
                self.board.pop()

                return beta

    def select_play(self):
        best_value = -99999
        best_play = ""

        for play in self.board.legal_moves:
            self.board.push(play)
            evaluation = self.minimax_alfabeta(alfa = -100000, beta = 100000)
            if evaluation > best_value:
                best_value = evaluation
                best_play = play
            
            self.board.pop()

        return best_play
