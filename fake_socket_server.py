import socket
import json
import numpy as np
import time
from envs.game_state import GameState, AgentInfo, GhostInfo, serialize_state
from envs import layouts
from config.socket_config import HOST, PORT



# -------------------------
# Fake game state (demo)
# -------------------------
fake_state = GameState(
    object_matrix=np.array([
        [layouts.WALL, layouts.WALL, layouts.WALL, layouts.WALL, layouts.WALL],
        [layouts.WALL, layouts.EMPTY, layouts.EMPTY, layouts.EMPTY, layouts.WALL],
        [layouts.WALL, layouts.EMPTY, layouts.PACMAN, layouts.EMPTY, layouts.WALL],
        [layouts.WALL, layouts.EMPTY, layouts.EMPTY, layouts.GHOST1, layouts.WALL],
        [layouts.WALL, layouts.WALL, layouts.WALL, layouts.WALL, layouts.WALL]
    ]),
    pacman=AgentInfo(x=2, y=2, dir=0),
    ghosts=[GhostInfo(x=3, y=3, dir=0, scared_timer=0)],
    score=0.0,
    win=False,
    lose=False
)

# -------------------------
# Socket server
# -------------------------
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print(f"[FakeServer] running on {HOST}:{PORT}")

    try:
        while True:
            conn, addr = s.accept()
            print(f"[FakeServer] Connected by {addr}")
            with conn:
                while True:
                    data = conn.recv(4096)
                    if not data:
                        break
                    try:
                        msg = json.loads(data.decode("utf-8"))
                    except json.JSONDecodeError:
                        continue

                    if msg.get("type") == "request_state":
                        # Send serialized game state
                        conn.sendall(json.dumps({
                            "type": "state",
                            "state": serialize_state(fake_state)
                        }).encode("utf-8"))
                        print(f"[FakeServer] Sent state to agent {msg.get('agent')}")
                    elif msg.get("type") == "action":
                        # Just print received action
                        print(f"[FakeServer] Received action from agent {msg.get('agent')}: {msg.get('action')}")
                    time.sleep(0.05)
    except KeyboardInterrupt:
        print("[FakeServer] Shutting down")
