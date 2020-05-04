from tictactoe import initial_state, player, actions, result, winner, utility, minimax
import helper

board = initial_state()

# player = player(board)
# print(player)
# actions = actions(board)
# print(actions)
# result = result(board,(0,2))
# print(result)
winner = winner(board)
print('winner')
print(winner)

utility = utility(board)
print('utility')
print(utility)

print('---Minimax---')
minimax = minimax(board)
print('----Best Move---')
print(minimax)
