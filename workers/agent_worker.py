import sys
import time
from envs.game_state import GameState, deserialize_state
from frontend.socket_client import SocketClient
from agents.factory import make_agent
from config.socket_config import HOST, PORT

STEP_SLEEP = 0.1

def main():
    if len(sys.argv) < 3:
        print("Usage: python agent_worker.py <agent_idx> <algo>")
        sys.exit(1)

    agent_idx = int(sys.argv[1])
    algo = sys.argv[2]

    agent = make_agent(algo, agent_idx)
    client = SocketClient(host=HOST, port=PORT)

    print(f"[Agent Worker {agent_idx}] started with algo '{algo}'")

    while True:
        try:
            # Yêu cầu trạng thái từ server
            client.send({"type": "request_state", "agent": agent_idx})
            raw_msg = client.recv()
            if not raw_msg or raw_msg.get("type") != "state":
                time.sleep(STEP_SLEEP)
                continue

            # Deserialize state (dạng struct mới)
            game_state: GameState = deserialize_state(raw_msg.get("state"))
            print(f"[Agent Worker {agent_idx}] received state")
            print(game_state)

            # Lấy action từ agent
            action = agent.getAction(game_state)
            print(f"[Agent Worker {agent_idx}] sending action: {action}")

            # Gửi action về server
            client.send({"type": "action", "agent": agent_idx, "action": action})
            time.sleep(STEP_SLEEP)

        except KeyboardInterrupt:
            print(f"[Agent Worker {agent_idx}] terminating.")
            break
        except Exception as e:
            print(f"[Agent Worker {agent_idx}] Error: {e}")
            time.sleep(STEP_SLEEP)

if __name__ == "__main__":
    main()
