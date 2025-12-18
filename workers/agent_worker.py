import random
import time
from envs.directions import Directions
from frontend.socket_client import get_state, send_action
from workers.state_adapter import adapt_state
from agents.factory import make_agent
import sys


STEP_SLEEP = 0.1  # Time to sleep between steps

def main():
    if len(*sys.argv) < 3:
        print("Usage: agent_worker.py <agent_idx> <algo>")
        sys.exit(1)

    agent_idx = int(sys.argv[1])
    algo = sys.argv[2]
    
    agent_code = 4 if agent_idx == 0 else 5 + (agent_idx - 1)

    agent = make_agent(algo, agent_idx)

    agent.registerInitialState(None)
    
    print(f"Agent Worker {agent_idx} started with algo '{algo}'")

    while True:
        try:
            raw_state = get_state()
            if not raw_state:
                time.sleep(STEP_SLEEP)
                continue

            obs = adapt_state(raw_state, agent_idx)
            action = agent.getAction(obs)
            if action is None:
                legal = obs.get("legal_actions", [])
                if legal:
                    action = random.choice(legal)
                else:
                    action = "North"

            send_action(agent_idx, action)
            time.sleep(STEP_SLEEP)

        except KeyboardInterrupt:
            print(f"Agent Worker {agent_idx} terminating.")
            break

        except Exception as e:
            print(f"Error in Agent Worker {agent_idx}: {e}")
            time.sleep(STEP_SLEEP)

if __name__ == "__main__":
    main()