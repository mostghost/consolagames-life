from tarfile import tar_filter
from modules import cg_input
from modules import cg_logic
from modules import cg_display

import time


input_manager = cg_input.CGInput()
logic_manager = cg_logic.CGLogic()
display_manager = cg_display.CGDisplay()

TARGET_FPS = 12
TARGET_DURATION = 1.0 / TARGET_FPS


while True:
    delta_start = time.time()

    input_manager.update()
    logic_manager.update()
    display_manager.update()

    delta_end = time.time()

    delta_elapsed = delta_end - delta_start
    delta_frame = TARGET_DURATION - delta_elapsed

    if delta_frame > 0:
        time.sleep(delta_frame)
