class CGLogic:
    def __init__(self):
        pass

    def update(self):

        grid = []

        with open("modules/display_test.txt", "r") as fh:
            for line in fh:
                line_list = line.strip().replace(" ", "").split(",")
                grid.append(line_list)

        return grid
