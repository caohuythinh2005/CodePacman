from frontend.socket_client import get_state, send_action
from workers.state_adapter import adapt_state

raw = get_state()
obs = adapt_state(raw, agent_code=4)

if raw is None:
    print("Socket chưa trả dữ liệu. Hãy chắc chắn controller đang chạy.")
else:
    obs = adapt_state(raw, agent_code=4)
    print("Pacman pos:", obs["position"])
    print("Legal actions:", obs["legal_actions"])