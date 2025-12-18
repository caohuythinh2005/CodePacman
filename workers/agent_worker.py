import sys
import time
import random
import numpy as np
from envs.game_state import GameState
from frontend.socket_client import SocketClient
from agents.random_agent import RandomAgent
from envs.game_state import deserialize_state

STEP_SLEEP = 0.1


def main():
    if len(sys.argv) < 3:
        print("Usage: python agent_worker.py <agent_idx> <algo>")
        sys.exit(1)

    agent_idx = int(sys.argv[1])
    algo = sys.argv[2]

    agent = RandomAgent()
    client = SocketClient()

    print(f"[Agent Worker {agent_idx}] started with algo '{algo}'")

    while True:
        try:
            client.send({"type": "request_state", "agent": agent_idx})
            raw_msg = client.recv()
            if not raw_msg or raw_msg.get("type") != "state":
                time.sleep(STEP_SLEEP)
                continue
            obs = deserialize_state(raw_msg.get("state"))
            print(f"[Agent Worker {agent_idx}] received state")
            print(obs)
            action = agent.getAction(obs)
            print(f"[Agent Worker {agent_idx}] sending action: {action}")
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
