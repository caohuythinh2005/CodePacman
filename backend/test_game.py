import sys
import os
import time

# 1. Đảm bảo PROJECT_ROOT nằm trong sys.path để các import hoạt động chính xác
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pacman_game import PacmanGame
from ui.impls.tkinter_ui import TkinterDisplay  # Cập nhật từ file gộp renderers.py

def run_test():
    """
    Chạy thử nghiệm tích hợp giữa logic game và UI gộp.
    Cho phép mở cửa sổ Tkinter mà không cần vòng lặp vô hạn.
    """
    # 2. Khởi tạo UI Tkinter
    ui = TkinterDisplay(zoom=1.5, frame_time=0.1)

    # 3. Khởi tạo Game với bản đồ mẫu
    map_path = os.path.join(PROJECT_ROOT, "maps", "mediumClassic.map")
    
    if not os.path.isfile(map_path):
        print(f"[Lỗi] Không tìm thấy file map tại {map_path}")
        return

    game = PacmanGame(map_path, display=ui)
    print("--- Bắt đầu Test UI (Phiên bản gộp) ---")
    
    # 4. Giả lập một chuỗi hành động của Pacman
    actions = ["East", "East", "East", "North", "North", "West", "West"]
    
    for action in actions:
        if game.check_game_over():
            break

        # Thực hiện hành động Pacman
        game.apply_action(0, action)
        
        # Tăng điểm để kiểm tra hiển thị score
        game.state.score += 10

        # Pause để người dùng quan sát chuyển động
        time.sleep(0.5)

    print("--- Test hoàn tất. Cửa sổ vẫn mở, nhấn đóng để kết thúc ---")

    # Khi muốn đóng thủ công, gọi finish
    # ui.finish()  # Có thể comment để giữ cửa sổ mở
    # Nếu muốn tự động đóng:
    # ui.finish()

if __name__ == "__main__":
    run_test()
