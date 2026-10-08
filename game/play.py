import json
import sys
import os

ROWS = 6
COLS = 7

def check_win(board, piece):
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c+i] == piece for i in range(4)):
                return True
    # Vertical
    for r in range(ROWS - 3):
        for c in range(COLS):
            if all(board[r+i][c] == piece for i in range(4)):
                return True
    # Positive diagonal
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True
    # Negative diagonal
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True
    return False

def render_board_markdown(state):
    board = state["board"]
    turn = state["turn"]
    winner = state["winner"]
    last_player = state.get("lastPlayer", "None")
    moves = state.get("moves", 0)

    # Emoji map: 0 = empty (⚪), 1 = Red (🔴), 2 = Yellow (🟡)
    emoji_map = {0: "⚪", 1: "🔴", 2: "🟡"}
    turn_name = "🔴 **Red**" if turn == 1 else "🟡 **Yellow**"

    lines = []
    lines.append("<div align=\"center\">")
    lines.append("")
    lines.append("## 🎮 Community Connect Four")
    lines.append("")
    
    if winner == 0 and moves < ROWS * COLS:
        lines.append(f"**Current Turn:** {turn_name} &nbsp; | &nbsp; **Last Move By:** <a href=\"https://github.com/{last_player}\">**@{last_player}**</a> &nbsp; | &nbsp; **Moves:** {moves}")
    elif winner != 0:
        win_name = "🔴 **Red**" if winner == 1 else "🟡 **Yellow**"
        lines.append(f"🎉 **Game Over! {win_name} Won!** (Won by <a href=\"https://github.com/{last_player}\">**@{last_player}**</a>) — [**🔄 Play Again**](https://github.com/rugved-danej/rugved-danej/issues/new?template=connect4.yml&title=Connect+Four+Move&move=Reset+Game)")
    else:
        lines.append(f"🤝 **Game Over! It's a Tie!** — [**🔄 Play Again**](https://github.com/rugved-danej/rugved-danej/issues/new?template=connect4.yml&title=Connect+Four+Move&move=Reset+Game)")

    lines.append("")
    
    # Header with column drop buttons using numbers
    number_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣"]
    cols_header = []
    for c in range(COLS):
        col_num = c + 1
        link = f"[{number_emojis[c]}](https://github.com/rugved-danej/rugved-danej/issues/new?template=connect4.yml&title=Connect+Four+Move&move=Drop+in+Column+{col_num})"
        cols_header.append(link)
    
    lines.append("| " + " | ".join(cols_header) + " |")
    lines.append("| " + " | ".join([":---:"] * COLS) + " |")

    # Rows
    for r in range(ROWS):
        row_str = " | ".join([emoji_map[board[r][c]] for c in range(COLS)])
        lines.append(f"| {row_str} |")

    lines.append("")
    lines.append("<i>Click any number above to drop your disc! The board updates automatically.</i>")
    lines.append("")
    lines.append("</div>")
    return "\n".join(lines)

def update_readme(board_md):
    readme_path = "README.md"
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    start_tag = "<!-- CONNECT4_START -->"
    end_tag = "<!-- CONNECT4_END -->"

    if start_tag in content and end_tag in content:
        before = content.split(start_tag)[0]
        after = content.split(end_tag)[1]
        new_content = f"{before}{start_tag}\n\n{board_md}\n\n{end_tag}{after}"
    else:
        new_content = content + f"\n\n{start_tag}\n\n{board_md}\n\n{end_tag}\n"

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)

def main():
    action = sys.argv[1] if len(sys.argv) > 1 else ""
    user = sys.argv[2] if len(sys.argv) > 2 else "Anonymous"

    state_file = "game/connect4.json"
    if not os.path.exists(state_file):
        state = {"board": [[0]*COLS for _ in range(ROWS)], "turn": 1, "winner": 0, "lastPlayer": "None", "moves": 0}
    else:
        with open(state_file, "r") as f:
            state = json.load(f)

    if action == "reset":
        state = {"board": [[0]*COLS for _ in range(ROWS)], "turn": 1, "winner": 0, "lastPlayer": user, "moves": 0}
    elif action.startswith("drop"):
        try:
            col = int(action.split("|")[1]) - 1
            if 0 <= col < COLS and state["winner"] == 0:
                # Find lowest empty row in col
                placed = False
                for r in reversed(range(ROWS)):
                    if state["board"][r][col] == 0:
                        state["board"][r][col] = state["turn"]
                        state["moves"] = state.get("moves", 0) + 1
                        state["lastPlayer"] = user
                        placed = True
                        if check_win(state["board"], state["turn"]):
                            state["winner"] = state["turn"]
                        else:
                            state["turn"] = 2 if state["turn"] == 1 else 1
                        break
        except Exception as e:
            print(f"Invalid move: {e}")

    with open(state_file, "w") as f:
        json.dump(state, f)

    board_md = render_board_markdown(state)
    update_readme(board_md)
    print("Board updated successfully!")

if __name__ == "__main__":
    main()
