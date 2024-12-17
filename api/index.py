
from flask import Flask, request, jsonify

app = Flask(__name__)

# Global variables for game state
player = "o"
opponent = "x"
board = [['_' for _ in range(3)] for _ in range(3)]

@app.route('/new_game', methods=['POST'])
def new_game():
    global board, player, opponent
    data = request.json
    player = data.get('player', 'o')
    opponent = 'x' if player == 'o' else 'o'
    board = [['_' for _ in range(3)] for _ in range(3)]
    return jsonify({"message": "Game initialized", "board": board})

@app.route('/move', methods=['POST'])
def make_move():
    global board
    data = request.json
    board = data['board']
    is_human_turn = data['is_human_turn']

    if is_human_turn:
        move = data['move']
        board[move[0]][move[1]] = opponent
    else:
        from tic_tac_toe import find_best_move  # Import from your game logic
        move = find_best_move(board)
        board[move[0]][move[1]] = player

    winner = check_winner(board)  # Check the winner
    return jsonify({"board": board, "winner": winner, "ai_move": move})

def check_winner(board):
    """Returns the result of the game."""
    score = evaluate(board)
    if score == 10:
        return "AI wins!"
    elif score == -10:
        return "Human wins!"
    elif not is_moves_left(board):
        return "It's a draw!"
    return None

if __name__ == '__main__':
    app.run(debug=True)
