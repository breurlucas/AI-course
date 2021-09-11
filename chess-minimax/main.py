# Beatriz Paiva & Lucas Breur
# Senac 2021 - Artificial Intelligence course

from chess_minimax import Bot
import random

game = Bot()

print("\nLet's play Chess\n")
print(game.board,"\n")

while not game.board.is_game_over(claim_draw=False):

    if game.board.turn:
        play = game.select_play()
        game.board.push(play)
        print("Bot has played ", play, "\n")
        print(game.board,"\n")
    else:
        # Random play for testing purposes
        p_play = random.choice([play for play in game.board.legal_moves])
        game.board.push(p_play)
        print("Player has played ", play, "\n")
        print(game.board,"\n")

        # p_play = input("Your move player: ")
        # print()
        # game.board.push_san(p_play)
        # print(game.board,"\n")

# If one of the players won, check which one
if game.board.is_checkmate():
    if game.board.turn:
        print("Congratulations, you won!")
    else:
        print("Better luck next time..")

# Draw
if game.board.is_stalemate():
    print("Draw!")
if game.board.is_insufficient_material():
    print("Draw!")

# Fivefold Repetition or Seventyfive Moves (July 2014 rules)
print(game.board.outcome())