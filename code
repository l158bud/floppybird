# FloppyCircle — a tiny text Flappy clone for TI-Nspire CX II Python
# Controls: 'w' + Enter = flap, just Enter = no flap
# Turn-based to work nicely with the calculator's input()

import random, time

# --- Config ---
H = 12            # screen height (rows)
W = 28            # screen width (cols)
PLAYER_X = 6      # fixed column for the player
GAP = 3           # pipe gap height
SPAWN_EVERY = 3   # ticks between new pipes
MAX_VEL_DOWN = 2  # terminal fall speed
FLAP_IMPULSE = -2 # up velocity when flapping

# --- State ---
player_y = H // 2
vel = 0
tick = 0
score = 0
best = 0
pipes = []  # list of dicts: {'x': int, 'gap_top': int}

def clear():
    # Simple "clear" for calc console
    print("\n" * 20)

def spawn_pipe():
    # Keep a 1-cell margin from top/bottom
    top = random.randint(1, H - GAP - 1)
    pipes.append({'x': W - 1, 'gap_top': top})

def move_pipes():
    for p in pipes:
        p['x'] -= 1
    # Remove pipes that moved off screen
    while pipes and pipes[0]['x'] < -1:
        pipes.pop(0)

def make_grid():
    # Start empty
    g = [[" "] * W for _ in range(H)]
    # Draw pipes
    for p in pipes:
        x = p['x']
        if 0 <= x < W:
            gt = p['gap_top']
            for y in range(H):
                if not (gt <= y < gt + GAP):
                    g[y][x] = "#"
    # Draw player
    if 0 <= PLAYER_X < W and 0 <= player_y < H:
        g[player_y][PLAYER_X] = "O"  # the FloppyCircle :)
    return g

def collided():
    # Off-screen = crash
    if player_y < 0 or player_y >= H:
        return True
    # Hit a pipe?
    for p in pipes:
        if p['x'] == PLAYER_X:
            gt = p['gap_top']
            if not (gt <= player_y < gt + GAP):
                return True
    return False

def draw(grid, msg=""):
    clear()
    print("+{}+".format("-"*W))
    for row in grid:
        print("|" + "".join(row) + "|")
    print("+{}+".format("-"*W))
    print("Score:", score, "  Best:", best)
    if msg:
        print(msg)

def prompt():
    # Read one line; 'w' to flap, anything else = no flap
    try:
        s = input("[Enter]=fall   w+Enter=flap   q=quit > ").strip().lower()
    except:
        s = ""
    return s

def step(flapped):
    global player_y, vel, score, tick
    # Gravity / flap
    if flapped:
        vel = FLAP_IMPULSE
    else:
        vel += 1
    if vel > MAX_VEL_DOWN:
        vel = MAX_VEL_DOWN
    player_y += vel

    # Pipes
    if tick % SPAWN_EVERY == 0:
        spawn_pipe()
    move_pipes()

    # Score when you safely pass the pipe column
    for p in pipes:
        if p['x'] == PLAYER_X - 1 and 0 <= player_y < H:
            score += 1
            break

    tick += 1

def game_loop():
    global player_y, vel, tick, score, best, pipes
    # Reset state
    player_y = H // 2
    vel = 0
    tick = 0
    score = 0
    pipes = []

    while True:
        grid = make_grid()
        draw(grid)
        s = prompt()
        if s == "q":
            return False  # quit to title
        flapped = (s == "w")

        step(flapped)

        if collided():
            if score > best:
                best = score
            grid = make_grid()
            draw(grid, msg="💥 Crash!  Final score: {}   (Best: {})".format(score, best))
            time.sleep(0.6)
            # Post-crash menu
            try:
                again = input("Play again? (y/n) > ").strip().lower()
            except:
                again = "n"
            return (again == "y")

def title():
    clear()
    print("+{}+".format("="*W))
    name = "  F L O P P Y C I R C L E  "
    pad = (W - len(name))//2
    line = " "*pad + name + " "*max(0, W - len(name) - pad)
    print("|" + line + "|")
    print("+{}+".format("="*W))
    print("Survive by flapping through the # pipes.")
    print("Controls: 'w' + Enter to flap, just Enter to fall, 'q' to quit.")
    print("")
    try:
        _ = input("Press Enter to start... ")
    except:
        pass

# --- Run ---
while True:
    title()
    keep = game_loop()
    if not keep:
        clear()
        print("Thanks for playing FloppyCircle! Final Best:", best)
        break
