class Table():


    def __init__(self):
        self.grid = [["~", "~", "~"], ["~", "~", "~"], ["~", "~", "~"]]

    def checkspacefree(self, x, y):
        return self.grid[y][x] == "~"

    def __checkwinrow(self, charac):
        for row in self.grid:
            completed = True
            for item in row:
                if item != charac:
                    completed = False
            if completed:
                return True
        return False

    def __checkwincolumn(self, charac):
        leng = len(self.grid[0])
        for i in range(leng):
            completed = True
            for row in self.grid:
                if row[i] != charac:
                    completed = False
            if completed:
                return True
        return False

    def __checkwindiagtl(self, charac):
        for row in range(len(self.grid)):
            if self.grid[row][row] != charac:
                return False
        return True

    def __checkwindiagtr(self, charac):
        leng = len(self.grid[0])
        leng -= 1
        for row in range(len(self.grid)):
            if self.grid[row][leng - row] != charac:
                return False
        return True

    def __checkdraw(self):
        for row in self.grid:
            for item in row:
                if item == "~":
                    return False
        return True

    def checkwin(self):
        for charac in ["X", "O"]:
            winrows = self.__checkwinrow(charac)
            wincols = self.__checkwincolumn(charac)
            windiagtl = self.__checkwindiagtl(charac)
            windiagtr = self.__checkwindiagtr(charac)

            if winrows or wincols or windiagtl or windiagtr:

                return True, charac
        drawed = self.__checkdraw()

        return drawed, "~"

    def play(self, x, y, isX):
        if isX:
            self.grid[y][x] = "X"
        else:
            self.grid[y][x] = "O"