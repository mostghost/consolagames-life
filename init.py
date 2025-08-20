from modules import cg_input
from modules import cg_logic
from modules import cg_display

import time
import platform

if platform.system() != "Windows":
    import sys
    import termios
    import fcntl

    # We're making a copy of the original terminal settings to restore once we're done.
    # We're doing that because the input method on linux must mess with these to work.
    fd = sys.stdin.fileno()
    old_term = termios.tcgetattr(fd)
    old_flags = fcntl.fcntl(fd, fcntl.F_GETFL)

input_manager = cg_input.CGInput()
logic_manager = cg_logic.CGLogic()
display_manager = cg_display.CGDisplay()

TARGET_FPS = 12
TARGET_DURATION = 1.0 / TARGET_FPS

FRAME_COUNT = 0

try:
    while True:
        delta_start = time.time()

        inp = input_manager.update()
        # One special exception as soon as we get input:
        if inp == "O":
            sys.exit()

        grid, paused, cursor = logic_manager.update(q)
        display_manager.update(FRAME_COUNT, grid, paused, cursor)
        print(inp)
        print(cursor)

        delta_end = time.time()

        delta_elapsed = delta_end - delta_start
        delta_frame = TARGET_DURATION - delta_elapsed

        if delta_frame > 0:
            time.sleep(delta_frame)

        FRAME_COUNT += 1
finally:
    if platform.system() != "Windows":
        termios.tcsetattr(fd, termios.TCSANOW, old_term)
        fcntl.fcntl(fd, fcntl.F_SETFL, old_flags)
