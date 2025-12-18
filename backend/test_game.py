import sys
import os
import time
import random

# 1. Đảm bảo PROJECT_ROOT nằm trong sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pacman_game import PacmanGame
from ui.impls.tkinter_ui import TkinterDisplay

def load_actions(file_path):
    """Đọc file action từ đường dẫn"""
    if not os.path.isfile(file_path):
        print(f"[Lỗi] Không tìm thấy file action tại {file_path}")
        return []
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def run_test():
    ui = TkinterDisplay(zoom=1.5, frame_time=0.1)

    # --- File map ---
    map_path = os.path.join(PROJECT_ROOT, "maps", "mediumClassic.map")
    if not os.path.isfile(map_path):
        print(f"[Lỗi] Không tìm thấy file map tại {map_path}")
        return

    game = PacmanGame(map_path, display=ui)
    print("--- Bắt đầu Test UI ---")

    # --- File action ---
    action_path = os.path.join(PROJECT_ROOT, "actions", "pacman_actions.txt")
    pacman_actions = load_actions(action_path)
    if not pacman_actions:
        print("[Lỗi] Không có action nào để thực hiện.")
        return

    for action in pacman_actions:
        if game.check_game_over():
            break

        game.apply_action(0, action)

        # Ghosts di chuyển ngẫu nhiên
        for idx in range(1, 1 + game.state.num_ghosts()):
            legal = game.state.getLegalActions(idx)
            if legal:
                ghost_action = random.choice(legal)
                game.apply_action(idx, ghost_action)

        # Tăng điểm để kiểm tra hiển thị score
        game.state.score += 10
        time.sleep(0.1)

    print("--- Test hoàn tất. Cửa sổ vẫn mở, nhấn đóng để kết thúc ---")

if __name__ == "__main__":
    run_test()
