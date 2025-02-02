from ..display.Colors import Colors as Col

def print_state(state):

    print(f"{Col.CYAN}{Col.BOLD}Snake state{Col.END}")
    print(f"{Col.BOLD}{Col.YELLOW}\tWall", end="")
    print(f"{Col.BOLD}{Col.GREEN}\t\t\tGreen fruit ", end="")
    print(f"{Col.BOLD}{Col.RED}\t\tRed fruit  ", end="")
    print(f"{Col.BOLD}{Col.MAGENTA}\t\tBody  ")
    
    print(f"{Col.BOLD}{Col.YELLOW}", end="")
    print(f"[{state[0]:.2f}, {state[1]:.2f}, {state[2]:.2f}, {state[3]:.2f}]", end="")
    print(f"{Col.GREEN}", end="")
    print(f"[{state[4]:.2f}, {state[5]:.2f}, {state[6]:.2f}, {state[7]:.2f}]", end="")
    print(f"{Col.RED}", end="")
    print(f"[{state[8]:.2f}, {state[9]:.2f}, {state[10]:.2f}, {state[11]:.2f}]", end="")
    print(f"{Col.MAGENTA}", end="")
    print(f"[{state[12]:.2f}, {state[13]:.2f}, {state[14]:.2f}, {state[15]:.2f}]")
    print(Col.END)

def print_experience(state, action, reward, done):
    print_state(state)
    actions = {0: "UP", 1: "DOWN", 2 : "LEFT", 3 : "RIGHT"}
    print(f"Action: {actions[action]} | Reward: {reward} | Done: {done}")