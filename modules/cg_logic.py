class CGLogic:
    def __init__(self):
        self.old_grid = []
        self.update_grid = []

        with open("modules/display_test.txt", "r") as fh:
            for line in fh:
                line_list = line.strip().replace(" ", "").split(",")
                self.old_grid.append(line_list)

        self._grid_to_int()

    def update(self):

        self.update_grid = []

        for l_index, line in enumerate(self.old_grid):
            if l_index == 0 or l_index == (len(self.old_grid) - 1):
                # We want to maintain a border of '0's around the edge of the grid,
                # so we'll skip updating the first and last lines.
                new_line = [0 for x in range(len(line))]
                self.update_grid.append(new_line)
                continue
            else:
                new_line = [0]
                # We also want to skip the first and last character of each line and
                # pad those characters out with 0's as well.
                for c_index, char in enumerate(line):
                    if c_index == 0 or c_index == len(line) - 1:
                        continue
                    else:

                        population = self.old_grid[l_index - 1][c_index - 1]
                        population += self.old_grid[l_index - 1][c_index]
                        population += self.old_grid[l_index - 1][c_index + 1]
                        population += self.old_grid[l_index][c_index - 1]
                        population += self.old_grid[l_index][c_index + 1]
                        population += self.old_grid[l_index + 1][c_index - 1]
                        population += self.old_grid[l_index + 1][c_index]
                        population += self.old_grid[l_index + 1][c_index + 1]

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
                self.update_grid.append(new_line)

        self.old_grid = self.update_grid

        self._grid_to_str()

        return self.update_grid

    def _grid_to_str(self):
        grid_replacer = []

        for line in self.update_grid:
            grid_replacer.append([str(x) for x in line])

        self.update_grid = grid_replacer

    def _grid_to_int(self):
        grid_replacer = []

        for line in self.old_grid:
            grid_replacer.append([int(x) for x in line])

        self.old_grid = grid_replacer
