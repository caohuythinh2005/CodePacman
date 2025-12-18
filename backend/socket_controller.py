import sys
import os
import socket
import json
import threading
from datetime import datetime

# Ensure project root is on sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pacman_game import PacmanGame
from config.socket_config import HOST, PORT

# -------------------------------
# Paths
# -------------------------------
BASE_DIR = os.path.dirname(__file__)
LOG_DIR = os.path.join(BASE_DIR, "../logs")
os.makedirs(LOG_DIR, exist_ok=True)

STATE_LOG_FILE = os.path.join(LOG_DIR, "states.jsonl")
ACTION_LOG_FILE = os.path.join(LOG_DIR, "actions.jsonl")

log_lock = threading.Lock()

# -------------------------------
# Game init (ENGINE ONLY)
# -------------------------------
MAP_FILE = os.path.join(BASE_DIR, "../maps/mediumClassic.map")
game = PacmanGame(MAP_FILE)

# -------------------------------
# Utils
# -------------------------------
def read_latest_state_from_log():
    """Read last JSON line from states.jsonl"""
    if not os.path.exists(STATE_LOG_FILE):
        return None

    with open(STATE_LOG_FILE, "rb") as f:
        try:
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b"\n":
                f.seek(-2, os.SEEK_CUR)
        except OSError:
            f.seek(0)

        line = f.readline().decode("utf-8").strip()
        return json.loads(line) if line else None


def log_action(agent_idx, action):
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "agent": agent_idx,
        "action": action
    }
    with log_lock:
        with open(ACTION_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

# -------------------------------
# Socket handler
# -------------------------------
def handle_client(conn, addr):
    print(f"[Backend] New connection from: {addr}")
    buffer = ""

    try:
        while True:
            data = conn.recv(8192)
            if not data:
                print(f"[Backend] {addr} disconnected.")
                break

            buffer += data.decode("utf-8")

            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                if not line.strip():
                    continue

                try:
                    msg = json.loads(line)
                except json.JSONDecodeError:
                    print(f"[Backend] JSONDecodeError from {addr}: {line}")
                    continue

                msg_type = msg.get("type")

                # -----------------------
                # REQUEST STATE
                # -----------------------
                if msg_type == "request_state":
                    state = read_latest_state_from_log()
                    res = {
                        "type": "state",
                        "state": state
                    }
                    conn.sendall((json.dumps(res) + "\n").encode("utf-8"))

                # -----------------------
                # ACTION
                # -----------------------
                elif msg_type == "action":
                    agent_idx = msg.get("agent")
                    action = msg.get("action")

                    game.apply_action(agent_idx, action)
                    log_action(agent_idx, action)

                # -----------------------
                # STATUS
                # -----------------------
                elif msg_type == "get_status":
                    res = {
                        "type": "status",
                        "last_executed": game.last_actions
                    }
                    conn.sendall((json.dumps(res) + "\n").encode("utf-8"))

                else:
                    print(f"[Backend] Unknown message type: {msg_type}")

    except ConnectionResetError:
        print(f"[Backend] {addr} disconnected abruptly.")
    finally:
        conn.close()

# -------------------------------
# Server
# -------------------------------
def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(20)

    print(f"--- BACKEND SERVER --- Running at {HOST}:{PORT}")
    print(f"[Backend] State source : {STATE_LOG_FILE}")
    print(f"[Backend] Action log  : {ACTION_LOG_FILE}")

    try:
        while True:
            conn, addr = s.accept()
            threading.Thread(
                target=handle_client,
                args=(conn, addr),
                daemon=True
            ).start()
    except KeyboardInterrupt:
        print("\n[Backend] Shutting down server...")
    finally:
        s.close()

# -------------------------------
# Main
# -------------------------------
if __name__ == "__main__":
    start_server()
