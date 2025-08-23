# 🐦 FLOPPYCIRCLE — A TI‑Nspire CX II Mini‑Game

A Flappy‑style parody for the TI‑Nspire CX II, written in Python.  
Navigate your floppy circle through pipes and try to hit the max score of **100**!

---

## 📥 Installation

1. On your TI‑Nspire CX II, press **[doc]**.  
2. Choose: **1: New Document → 4: Add Application → Python**.  
3. Copy the Python code into the editor, **or** transfer the included `.tns` file via:
   - **TI‑Nspire Student Software**, or  
   - **TI‑Nspire CX II Connect** (https://nspireconnect.ti.com).

> Optional: In **File → Document Properties → Protection**, set the document to **Read‑Only** so players are prompted to **Save As** instead of overwriting your original.

---

## ▶️ How to Run

- In the Python editor, press **[ctrl] + [R]** to run.  
- The title screen will appear; press **[Enter]** to start.  

---

## 🎮 Controls

- **[1]** = Flap upward  
- **[2]** = Do nothing (gravity pulls you down)  
- **[9]** = Quit game  

---

## 🎯 Goal & Rules

- The gameplay view shows the **bottom 8 rows** of the world (no invisible space).  
- Survive and pass through `#` pipes to score points.  
- Difficulty ramps up over time (smaller gaps, tighter spacing).  
- The run **ends at 100 points** with a win screen.  
- Your **best score** is remembered until you quit the session.

---

## 🧩 Tuning Knobs (inside code)

- `GRAVITY`, `FLAP_IMPULSE`, `MAX_VEL_DOWN` — feel of flight  
- `GAP_START`, `GAP_MIN` — initial vs. minimum gap size  
- `SPAWN_EVERY_EASY/HARD` — pipe spacing early vs. later  

---

## 👤 Author

Created by **l158bud** with help from ChatGPT (play‑feel tuning & code cleanup). discord: https://discord.gg/QFQn3NVV6U
