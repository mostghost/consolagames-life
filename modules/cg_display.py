import os


class CGDisplay:

    def __init__(self):
        self.fps_next = 3  # The game starts at '2', or 12FPS.
        # It cycles from 1-4. 8 and 9 are special cases for pausing and unpausing.
        self.fps_store = 0
        self.paused = False

        self.target_fps = 12
        self.target_duration = 1.0 / 12

        self.append_block = []
        self.append_block_paused = []

    def change_fps(self):

        match self.fps_next:
            case 1:
                TARGET_FPS = 8
                TARGET_DURATION = 1.0 / 8
                self.fps_next += 1

            case 2:
                TARGET_FPS = 12
                TARGET_DURATION = 1.0 / 12
                self.fps_next += 1

            case 3:
                TARGET_FPS = 24
                TARGET_DURATION = 1.0 / 24
                self.fps_next += 1

            case 4:
                TARGET_FPS = 48
                TARGET_DURATION = 1.0 / 48
                self.fps_next = 1

            case 8:  # Just paused
                TARGET_FPS = 60
                TARGET_DURATION = 1.0 / 60

            case 9:  # Just unpaused
                self.fps_store -= 1
                if self.fps_store == 0:
                    self.fps_store = 4
                self.fps_next = self.fps_store

                # Running through this function again will grab the appropriate values.
                TARGET_FPS, TARGET_DURATION = self.change_fps()

        self.target_fps = TARGET_FPS
        self.target_duration = TARGET_DURATION

        return TARGET_FPS, TARGET_DURATION

    def update(self, frame_count: int, grid: list, paused: bool, cursor: tuple):

        if self.paused != paused:  # Pause was toggled last frame.
            if self.paused is False and paused is True:
                self.paused = True
                self.fps_store = self.fps_next
                self.fps_next = 8
                return True
            elif self.paused is True and paused is False:
                self.paused = False
                self.fps_next = 9
                return True

        grid_formatted = self._format(grid)

        # Wipe the terminal clear before starting a new frame
        os.system("cls" if os.name == "nt" else "clear")

        if paused:
            grid_formatted = self._place_cursor(grid_formatted, cursor)

        for line in grid_formatted:
            print(line)

        if not self.append_block:
            line_length = len(grid_formatted[0])
            self._get_append_block(line_length)
            self._get_append_paused(line_length)

        if paused:
            for line in self.append_block_paused:
                print(line)
        else:
            for line in self.append_block:
                print(line)

    def _format(self, grid: list):

        new_grid = []

        for index, line in enumerate(grid):
            if index == 0:
                start_line = []
                start_line.extend(["╭"])
                start_line.extend(["─" for x in range((len(line) * 2) - 2)])
                start_line.extend(["╮"])
                new_grid.append("".join(start_line))
                continue
            elif index == len(grid) - 1:
                end_line = []
                end_line.extend(["├"])
                end_line.extend(["─" for x in range((len(line) * 2) - 2)])
                end_line.extend(["┤"])
                new_grid.append("".join(end_line))
                continue
            else:
                mid_line = []
                mid_line.extend(["│ "])
                new_line = ["██" if x == "1" else "  " for x in line[1:-1]]
                mid_line.extend(new_line)
                mid_line.extend([" │"])
                new_grid.append("".join(mid_line))
                continue

        return new_grid

    def _place_cursor(self, grid: list, cursor: tuple):
        x, y = cursor

        if grid[y][x * 2] == "█":
            cursor_replacement = "▓▓"
        elif grid[y][x * 2] == " ":
            cursor_replacement = "░░"

        grid[y] = grid[y][: x * 2] + cursor_replacement + grid[y][x * 2 + 2 :]

        return grid

    def _get_append_paused(self, length: int):
        line_wasd = "W, A, S, D to move cursor"
        line_space = "Space to toggle a cell"
        line_q = "Q to go back to Live Mode"
        pause_ender = " ▋ ▋         │"

        blank_space = " " * (length - 2 - 2 - len(line_wasd))
        one = "│ " + line_wasd + blank_space + " │"

        blank_space = " " * (length - 2 - len(line_space) - len(pause_ender))
        two = "│ " + line_space + blank_space + pause_ender

        blank_space = " " * (length - 2 - len(line_q) - len(pause_ender))
        three = "│ " + line_q + blank_space + pause_ender

        blank_space = " " * (length - 2 - len(pause_ender))
        four = "│ " + blank_space + pause_ender

        blank_space = " " * (length - 2 - 2)
        five = "│ " + blank_space + " │"

        six = "╰" + ("─" * (length - 2)) + "╯"

        self.append_block_paused.append(one)
        self.append_block_paused.append(two)
        self.append_block_paused.append(three)
        self.append_block_paused.append(four)
        self.append_block_paused.append(five)
        self.append_block_paused.append(six)



    def _get_append_block(self, length: int):
        line_q = "Q to Place Blocks"
        line_o = "O to Exit"
        line_v = "V for preset - Blank"
        line_b = "B for preset - Zigzag"
        line_n = "N for preset - Explosion"
        line_m = "M for preset - Gliders"
        line_z = f"Z to change FPS"

        blank_space = " " * (length - 2 - 2 - len(line_q) - len(line_o))
        one = "│ " + line_q + blank_space + line_o + " │"

        blank_space = " " * (length - 2 - 2 - len(line_v))
        two = "│ " + blank_space + line_v + " │"

        blank_space = " " * (length - 2 - 2 - len(line_b))
        three = "│ " + blank_space + line_b + " │"

        blank_space = " " * (length - 2 - 2 - len(line_n))
        four = "│ " + blank_space + line_n + " │"

        blank_space = " " * (length - 2 - 2 - len(line_m) - len(line_z))
        five = "│ " + line_z + blank_space + line_m + " │"

        six = "╰" + ("─" * (length - 2)) + "╯"

        self.append_block.append(one)
        self.append_block.append(two)
        self.append_block.append(three)
        self.append_block.append(four)
        self.append_block.append(five)
        self.append_block.append(six)
