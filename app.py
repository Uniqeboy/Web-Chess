from flask import Flask, jsonify, render_template, request
from chess_engine import create_game, is_valid_move, make_move, check_game_status

app = Flask(__name__)

# single source of truth for game state
game = create_game()
game["turn"] = "white"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/board")
def get_board():
    return jsonify(game["board"])


@app.route("/move", methods=["POST"])
def make_move_api():
    print("BEFORE MOVE, backend turn =", game["turn"])
    data = request.json

    ui_r1 = data["r1"]
    ui_c1 = data["c1"]
    ui_r2 = data["r2"]
    ui_c2 = data["c2"]

    turn = game["turn"]

    # convert UI → engine coordinates for black
    r1 = 7 - ui_r1 if turn == "black" else ui_r1
    c1 = ui_c1
    r2 = 7 - ui_r2 if turn == "black" else ui_r2
    c2 = ui_c2


    if not is_valid_move(game, r1, c1, r2, c2, turn):
        return jsonify({"error": "illegal move"}), 400

    # make move
    make_move(game, r1, c1, r2, c2)

    # switch turn (CRITICAL)
    game["turn"] = "black" if game["turn"] == "white" else "white"

    status = check_game_status(game, game["turn"])

    return jsonify({
        "board": game["board"],
        "next_turn": game["turn"],
        "status": status
    })


@app.route("/legal-moves", methods=["POST"])
def legal_moves_api():
    print("LEGAL MOVES REQUEST, backend turn =", game["turn"])
    data = request.json
    ui_r = data["r"]
    ui_c = data["c"]
    turn = game["turn"]

    # convert UI row to engine row for black
    r = 7 - ui_r if turn == "black" else ui_r
    c = ui_c

    moves = []

    for r2 in range(8):
        for c2 in range(8):
            if is_valid_move(game, r, c, r2, c2, turn):
                ui_r2 = 7 - r2 if turn == "black" else r2
                moves.append({"r": ui_r2, "c": c2})

    print("LEGAL MOVES for", turn, "from", (ui_r, ui_c), "=>", moves)
    return jsonify(moves)


if __name__ == "__main__":
    app.run(debug=True)
