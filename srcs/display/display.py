from ..display.Colors import Colors as Col


def print_state(state):
    """Print actual state (Debug mode)."""
    print(f"{Col.BOLD}Snake state")
    print(f"{Col.YELLOW}\tWall", end="")
    print(f"{Col.GREEN}\t\t\tGreen fruit ", end="")
    print(f"{Col.RED}\t\tRed fruit  ", end="")
    print(f"{Col.MAGENTA}\t\tBody  ", end="")
    print(f"{Col.CYAN}\t\t Collisions")

    print(f"{Col.BOLD}{Col.YELLOW}", end="")
    print(f"[{state[0]:.2f}, {state[1]:.2f}, ", end="")
    print(f"{state[2]:.2f}, {state[3]:.2f}]", end="")
    print(f"{Col.GREEN}", end="")
    print(f"[{state[4]:.2f}, {state[5]:.2f}, ", end="")
    print(f"{state[6]:.2f}, {state[7]:.2f}]", end="")
    print(f"{Col.RED}", end="")
    print(f"[{state[8]:.2f}, {state[9]:.2f}, ", end="")
    print(f"{state[10]:.2f}, {state[11]:.2f}]", end="")
    print(f"{Col.MAGENTA}", end="")
    print(f"[{state[12]:.2f}, {state[13]:.2f}, ", end="")
    print(f"{state[14]:.2f}, {state[15]:.2f}]", end="")
    print(f"{Col.CYAN}", end="")
    print(f"[{state[16]}, {state[17]}, {state[18]}, {state[19]}]")
    print(Col.END)


def print_experience(state, action, reward, done):
    """Print all parameters from step Q(s,a) to Q(s',a')."""
    print_state(state)
    actions = {0: "UP", 1: "DOWN", 2: "LEFT", 3: "RIGHT"}
    print(Col.BOLD, end="")
    print(f"Action: {Col.GREEN}{actions[action]}{Col.END}", end="")
    print(Col.BOLD, end="")
    print(" | Reward: ", end="")
    print(Col.GREEN if reward >= 0 else Col.RED, end="")
    print(f"{reward}{Col.END}", end="")
    print(Col.BOLD, end="")
    print(f" | Done: {Col.CYAN}{done}{Col.END}")
