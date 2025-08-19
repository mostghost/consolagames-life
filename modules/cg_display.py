import os
import pprint


class CGDisplay:
    def __init__(self):
        pass

    def update(self, frame_count: int, grid: list):

        # Wipe the terminal clear before starting a new frame
        os.system("cls" if os.name == "nt" else "clear")

        grid_formatted = self._format(grid)

        for line in grid_formatted:
            print(line)
        print(frame_count)

    def _format(self, grid: list):

        new_grid = []

        for index, line in enumerate(grid):
            if index == 0:
                start_line = []
                start_line.extend(["┏"])
                start_line.extend(["━" for x in range(len(line) - 2)])
                start_line.extend(["┓"])
                new_grid.append(''.join(start_line))
                continue
            elif index == len(grid) - 1:
                end_line = []
                end_line.extend(["┗"])
                end_line.extend(["━" for x in range(len(line) - 2)])
                end_line.extend(["┛"])
                new_grid.append(''.join(end_line))
                continue
            else:
                mid_line = []
                mid_line.extend(["┃"])
                new_line = ['█' if x == '1' else ' ' for x in line[1:-1]]
                mid_line.extend(new_line)
                mid_line.extend(["┃"])
                new_grid.append(''.join(mid_line))
                continue

        return new_grid
