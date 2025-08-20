class CGLogic:
    def __init__(self):
        self.old_grid = []
        self.pause_grid = []

        self.pause = False

        with open("modules/display_test.txt", "r") as fh:
            for line in fh:
                line_list = line.strip().replace(" ", "").split(",")
                self.old_grid.append(line_list)

        self.old_grid = self._grid_convert(self.old_grid, "int")

    def update(self, inp: str):
        if inp == "Q":
            self.pause = not self.pause

        if self.pause:
            # Pause logic
            return (self._grid_convert(self.old_grid, "str"), True)  # Grid, Pause
        else:
            updated_grid = self._run(self.old_grid)

            # By copying this before we convert the grid to a str, we can ensure that
            # the next frame we always have a clean int grid to work with.
            self.old_grid = updated_grid
            updated_grid = self._grid_convert(updated_grid, "str")

            return (updated_grid, False)  # Grid, Pause

    def _run(self, working_grid: list):
        updated_grid = []

        for l_index, line in enumerate(working_grid):
            if l_index == 0 or l_index == (len(working_grid) - 1):
                # We want to maintain a border of '0's around the edge of the grid,
                # so we'll skip updating the first and last lines.
                new_line = [0 for x in range(len(line))]
                updated_grid.append(new_line)
                continue
            else:
                new_line = [0]
                # We also want to skip the first and last character of each line and
                # pad those characters out with 0's as well.
                for c_index, char in enumerate(line):
                    if c_index == 0 or c_index == len(line) - 1:
                        continue
                    else:

                        population = working_grid[l_index - 1][c_index - 1]
                        population += working_grid[l_index - 1][c_index]
                        population += working_grid[l_index - 1][c_index + 1]
                        population += working_grid[l_index][c_index - 1]
                        population += working_grid[l_index][c_index + 1]
                        population += working_grid[l_index + 1][c_index - 1]
                        population += working_grid[l_index + 1][c_index]
                        population += working_grid[l_index + 1][c_index + 1]

                        if char == 1:
                            if population == 2 or population == 3:
                                new_line.extend([1])
                            else:
                                # Cell must be either overcrowded or undercrowded.
                                # And so cell dies.
                                new_line.extend([0])
                        elif char == 0:
                            if population == 3:
                                # If cell has 3 neighbours it reproduces.
                                new_line.extend([1])
                            else:
                                new_line.extend([0])
                # And add the last padding 0 for the end.
                new_line.extend([0])
                updated_grid.append(new_line)

        return updated_grid

    def _grid_convert(self, grid: list, grid_type: str):
        grid_converted = []

        if grid_type == "str":
            for line in grid:
                grid_converted.append([str(x) for x in line])
        elif grid_type == "int":
            for line in grid:
                grid_converted.append([int(x) for x in line])

        return grid_converted
