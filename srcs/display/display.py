from ..display.Colors import Colors as Col

def print_state(state):
        
    print("\n" + "="*50)
    print(f"{Col.CYAN}{Col.BOLD}Snake state:{Col.END}\n")
    
    print(f"{Col.YELLOW}{Col.BOLD}Wall distance:{Col.END}")
    print(f"Top: {state[0]:.3f} | Bottom: {state[7]:.3f} | Left: {state[14]:.3f} | Right: {state[21]:.3f}\n")
    
    # Fruits verts
    print(f"{Col.GREEN}{Col.BOLD}Green fruit:{Col.END}")
    print("\tTop\tBottom\tLeft\tRight")
    print(f"Mask:\t{state[1]:.0f}\t{state[8]:.0f}\t{state[15]:.0f}\t{state[22]:.0f}")
    print(f"Dist:\t{state[2]:.3f}\t{state[9]:.3f}\t{state[16]:.3f}\t{state[23]:.3f}\n")
    
    # Fruits rouges
    print(f"{Col.RED}{Col.BOLD}Red fruit:{Col.END}")
    print("\tTop\tBottom\tLeft\tRight")
    print(f"Mask:\t{state[3]:.0f}\t{state[10]:.0f}\t{state[17]:.0f}\t{state[24]:.0f}")
    print(f"Dist:\t{state[4]:.3f}\t{state[11]:.3f}\t{state[18]:.3f}\t{state[25]:.3f}\n")
    
    # Corps du serpent
    print(f"{Col.MAGENTA}{Col.BOLD}Snake body:{Col.END}")
    print("\tTop\tBottom\tLeft\tRight")
    print(f"Mask:\t{state[5]:.0f}\t{state[12]:.0f}\t{state[19]:.0f}\t{state[26]:.0f}")
    print(f"Dist:\t{state[6]:.3f}\t{state[13]:.3f}\t{state[20]:.3f}\t{state[27]:.3f}")
    
    print("="*50 + "\n")