import curses
import os
import time
import threading

import pygame

KEYS = {
    'a': 'kick.wav',
    's': 'snare.wav',
    'd': 'hihat_closed.wav',
    'f': 'hihat_open.wav',
    'j': 'tom_low.wav',
    'k': 'tom_mid.wav',
    'l': 'tom_high.wav',
    ';': 'crash.wav',
    "'": 'cowbell.wav',
}
SOUND_DIR = os.path.join(os.path.dirname(__file__), "sounds")

# Shared metronome state
metronome_on = False
bpm = 100
last_tick_time = 0

def metronome_loop(stdscr):
    global last_tick_time
    tick_interval = 60 / bpm
    while metronome_on:
        now = time.time()
        if now - last_tick_time >= tick_interval:
            last_tick_time = now
            stdscr.addstr(3, 2, f"Tick 🕒 ", curses.A_BOLD)
            stdscr.refresh()
            time.sleep(0.1)
            stdscr.addstr(3, 2, "         ")  # Clear tick
            stdscr.refresh()
        time.sleep(0.01)

def main(stdscr):
    global metronome_on, bpm, last_tick_time

    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(50)

    pygame.mixer.init()
    sounds = {k: pygame.mixer.Sound(os.path.join(SOUND_DIR, v)) for k, v in KEYS.items()}
    metronome_thread = None

    def draw_ui(active_key=None):
        stdscr.clear()
        stdscr.addstr(0, 0, "🎵 DrumTerm: Made for Tallant | Q to quit\n", curses.A_BOLD)
        for idx, key in enumerate(KEYS):
            line = f"[ {key.upper()} ] {KEYS[key].replace('.wav','').capitalize()}"
            if key == active_key:
                stdscr.addstr(idx + 5, 2, line, curses.A_REVERSE)
            else:
                stdscr.addstr(idx + 5, 2, line)
        stdscr.addstr(2, 2, f"Metronome: {'ON' if metronome_on else 'OFF'} | Tempo: {bpm} BPM (M: toggle metronome | +/-: tempo)" )
        stdscr.refresh()

    draw_ui()

    while True:
        try:
            key = stdscr.getch()
            if key == -1:
                continue

            key_chr = chr(key).lower()

            if key_chr == 'q':
                metronome_on = False
                break

            elif key_chr == 'm':
                metronome_on = not metronome_on
                last_tick_time = time.time()
                if metronome_on:
                    metronome_thread = threading.Thread(target=metronome_loop, args=(stdscr,))
                    metronome_thread.daemon = True
                    metronome_thread.start()

            elif key_chr == '+' and bpm < 300:
                bpm += 5
            elif key_chr == '-' and bpm > 30:
                bpm -= 5

            elif key_chr in sounds:
                sounds[key_chr].play()
                draw_ui(active_key=key_chr)
                time.sleep(0.1)
            draw_ui()

        except Exception as e:
            stdscr.addstr(10, 0, f"Error: {e}")
            stdscr.refresh()
            time.sleep(1)

    pygame.quit()

if __name__ == "__main__":
    curses.wrapper(main)

def run():
    curses.wrapper(main)
