# FloppyCircle — A TI‑Nspire CX II Flappy‑style parody
# Viewport: bottom 8 rows visible (no invisible space)
# Controls: 1 = flap, 2 = fall, 9 = quit
# Physics: smooth float gravity + flap impulse; “hard but fair” ramp
# Win: run ends at 100 points with a win screen

import random, time

# --- World / View Config ---
H = 11                 # total world rows (per your patch)
W = 28                 # world columns
VIEW_H = 8             # visible rows on the calculator
VIEW_TOP = H - VIEW_H  # index of first visible row (we show VIEW_TOP..H-1)

PLAYER_X = 6           # player's fixed column (horizontal)
WIN_SCORE = 100        # cap the run at 100 like the original end condition

# --- Physics (float / smoother) ---
# Units: rows per tick for velocity; rows per tick^2 for gravity
GRAVITY       = 0.35   # downward accel each tick
FLAP_IMPULSE  = -1.55  # upward velocity set when flapping
MAX_VEL_DOWN  = 1.80   # terminal fall speed (rows/tick)

# --- Difficulty (ramps to "hard but fair") ---
# Start with bigger gaps and then tighten as score increases
GAP_START     = 5
GAP_MIN       = 2
SPAWN_EVERY_EASY = 3   # columns between pipes at start
SPAWN_EVERY_HARD = 2   # tighter spacing later

# --- State ---
y = float(max(VIEW_TOP, H // 2))  # player y as float
vy = 0.0
tick = 0
score = 0
best = 0
pipes = []  # each: {'x': int, 'gap_top': int, 'gap_h': int}

def clear():
    print("\n" * 20)

def current_gap(score_):
    # Shrink gap by 1 every 10 points until GAP_MIN
    g = GAP_START - (score_ // 10)
    if g < GAP_MIN: g = GAP_MIN
    return g

def current_spawn_every(score_):
    # After 20 points, increase density
    return SPAWN_EVERY_EASY if score_ < 20 else SPAWN_EVERY_HARD

def spawn_pipe():
    gap = current_gap(score)
    # Keep the entire gap inside the visible 8 rows, with a safety margin
    top_min = max(1, VIEW_TOP)     # avoid top border
    top_max = H - gap - 1          # avoid bottom border
    if top_min > top_max:
        gt = max(VIEW_TOP + 1, 1)
    else:
        gt = random.randint(top_min, top_max)
    pipes.append({'x': W - 1, 'gap_top': gt, 'gap_h': gap})

def move_pipes():
    for p in pipes:
        p['x'] -= 1
    while pipes and pipes[0]['x'] < -1:
        pipes.pop(0)

def make_grid():
    grid = [[" "] * W for _ in range(H)]
    # Draw pipes
    for p in pipes:
        x = p['x']
        if 0 <= x < W:
            gt, gh = p['gap_top'], p['gap_h']
            for ry in range(H):
                if not (gt <= ry < gt + gh):
                    grid[ry][x] = "#"
    # Draw player (convert float y → int row)
    iy = int(round(y))
    if 0 <= PLAYER_X < W and 0 <= iy < H:
        grid[iy][PLAYER_X] = "O"
    return grid

def collided():
    # Bottom off-screen is a crash; top of visible window is a soft clamp
    if int(round(y)) >= H:
        return True
    # Pipe collision at player's column
    iy = int(round(y))
    for p in pipes:
        if p['x'] == PLAYER_X:
            gt, gh = p['gap_top'], p['gap_h']
            if not (gt <= iy < gt + gh):
                return True
    return False

def draw(grid, msg=""):
    clear()
    print("+{}+".format("-" * W))
    for row in grid[VIEW_TOP: H]:
        print("|" + "".join(row) + "|")
    print("+{}+".format("-" * W))
    print("Score:", score, "  Best:", best)
    if msg:
        print(msg)

def prompt():
    # 1 = flap, 2 = fall, 9 = quit (anything else = fall)
    try:
        s = input("[1]=flap   [2]=fall   [9]=quit > ").strip()
    except:
        s = ""
    if s == "1":
        return "flap"
    elif s == "9":
        return "quit"
    else:
        return "fall"

def step(flapped):
    global y, vy, score, tick
    # --- Physics ---
    if flapped:
        vy = FLAP_IMPULSE     # edge-triggered upward impulse
    else:
        vy += GRAVITY

    if vy >  MAX_VEL_DOWN: vy =  MAX_VEL_DOWN
    if vy < -MAX_VEL_DOWN: vy = -MAX_VEL_DOWN

    y += vy

    # Soft ceiling at the TOP of the VISIBLE window (never go into invisible space)
    if y < VIEW_TOP:
        y = float(VIEW_TOP)
        vy = 0.0

    # --- Pipes ---
    if tick % current_spawn_every(score) == 0:
        spawn_pipe()
    move_pipes()

    # --- Scoring (immediate, fair) ---
    iy = int(round(y))
    for p in pipes:
        if p['x'] == PLAYER_X and p['gap_top'] <= iy < p['gap_top'] + p['gap_h']:
            score += 1
            break

    tick += 1

def win_screen():
    clear()
    print("+{}+".format("=" * W))
    title = "  F L O P P Y   C I R C L E  "
    pad = (W - len(title)) // 2
    line = " " * pad + title + " " * max(0, W - len(title) - pad)
    print("|" + line + "|")
    print("+{}+".format("=" * W))
    print("🎉 You reached {}! Run complete.".format(WIN_SCORE))
    print("Final Best:", best)
    print("")
    try:
        _ = input("Press Enter to return to title... ")
    except:
        pass

def game_loop():
    global y, vy, tick, score, best, pipes
    # Reset per run
    y = float(max(VIEW_TOP, H // 2))
    vy = 0.0
    tick = 0
    score = 0
    pipes = []

    while True:
        grid = make_grid()
        draw(grid)
        s = prompt()
        if s == "quit":
            return False
        flapped = (s == "flap")

        step(flapped)

        # Win condition
        if score >= WIN_SCORE:
            if score > best:
                best = score
            grid = make_grid()
            draw(grid, msg="🏁 Reached {}! Nice flying.".format(WIN_SCORE))
            time.sleep(0.8)
            win_screen()
            return False

        if collided():
            if score > best:
                best = score
            grid = make_grid()
            draw(grid, msg="💥 Crash!  Final score: {}   (Best: {})".format(score, best))
            time.sleep(0.6)
            try:
                again = input("Play again? (y/n) > ").strip().lower()
            except:
                again = "n"
            return (again == "y")

def title():
    clear()
    print("+{}+".format("=" * W))
    name = "  F L O P P Y   C I R C L E  "
    pad = (W - len(name)) // 2
    line = " " * pad + name + " " * max(0, W - len(name) - pad)
    print("|" + line + "|")
    print("+{}+".format("=" * W))
    print("Visible area: bottom {} rows (of {} total).".format(VIEW_H, H))
    print("Goal: survive and reach {} points.".format(WIN_SCORE))
    print("Controls: 1 = flap, 2 = fall, 9 = quit.")
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
