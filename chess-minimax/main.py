# Beatriz Paiva & Lucas Breur
# Senac 2021 - Artificial Intelligence course

from chess_minimax import Bot

game = Bot()

print("\nLet's play Chess\n")
print(game.board,"\n")

while not game.board.is_game_over(claim_draw=True):
    if game.board.turn:
        play = game.select_play()
        game.board.push(play)
        print("Bot has played ", play, "\n")
        print(game.board,"\n")
    else:
        p_play = input("Your move player: ")
        print()
        game.board.push_san(p_play)
        print(game.board,"\n")
