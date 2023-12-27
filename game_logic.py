from typing import Dict, Tuple, Set, List

Position = Tuple[int, int]


class Minesweeper:
    def __init__(self, width: int, height: int,
                 mines: Dict[Position, int]):
        self.score: int = 0
        self.boundaries = width, height
        self.status: List[List[str]] = [[" " for i in range(width)]
                                        for i in range(height)]
        self.mines: Dict[Position, int] = mines
        self.area: Set[Position] = set()
        self.done: Set[Position] = set()


    def __valid(self, at: Position) -> bool:
        col, row = at
        width, height = self.boundaries
        if 0 <= col < width and 0 <= row < height:
            return True
        return False

    def __proxi(self, radius: int,  at: Position) -> Set[Position]:
        col, row = at
        valid_pos: Set[Position] = set()

        for add_col in range(-radius, radius + 1):
            for add_row in range(-radius, radius + 1):
                tile = (col + add_col, row + add_row)
                if self.__valid(tile) and tile != at:
                    valid_pos.add(tile)
        return valid_pos

    def __check_mines(self, searched: Set[Position]) -> str:
        near_mines: int = 0
        for at in searched:
            if self.mines.get(at) is not None:
                near_mines += 1
        return str(near_mines)

    def chain(self) -> None:
        while self.area:
            for tile in self.area:
                break
            col, row = tile
            self.uncover(col, row)

        return

    def uncover(self, col: int, row: int) -> None:
        tile: str = self.status[row][col]
        xy = (col, row)

        if tile == "F":
            return

        # mine click
        if self.mines.get(xy) is not None and tile == " ":
            self.status[row][col] = "*"
            self.score -= 10
            radius = self.mines.get(xy)
            self.done.add(xy)
            assert radius is not None  # just mypy stuff here
            self.area.update(self.__proxi(radius, xy))

            while self.area:
                for at in self.area:
                    break
                col, row = at
                self.area.remove(at)
                self.done.add(at)
                if self.status[row][col] == "*":
                    continue
                if self.mines.get(at) is not None:
                    self.uncover(col, row)
                else:
                    self.status[row][col] = "X"
            return

        # if unknown non-mine
        if tile == " ":
            tile = self.__check_mines(self.__proxi(1, xy))
            self.status[row][col] = tile
            self.score += 1
            if tile == "0":
                self.done.add(xy)
                self.area.update(self.__proxi(1, xy))
                self.area.difference_update(self.done & self.area)
                self.chain()

        # if uncoverd
        else:
            self.done.add(xy)
            if xy in self.area:
                self.area.remove(xy)
            if self.area:
                self.chain()
        return


    def flag(self, col: int, row: int) -> None:
        tile: str = self.status[row][col]
        xy = (col, row)

        if tile == " ":
            self.done.add(xy)
            self.status[row][col] = "F"
        if tile == "F":
            self.done.remove(xy)
            self.status[row][col] = " "
        return


def main() -> None:
    mines = {(2, 2): 5, (4, 5): 1, (6, 1): 0, (6, 3): 1, (6, 4): 3}

    ms = Minesweeper(8, 6, mines)
    assert ms.score == 0
    assert ms.status == [
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ]

    ms.uncover(1, 1)
    assert ms.score == 1
    assert ms.status == [
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', '1', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ]

    ms.uncover(0, 0)
    assert ms.score == 33
    assert ms.status == [
        ['0', '0', '0', '0', '0', '1', ' ', ' '],
        ['0', '1', '1', '1', '0', '1', ' ', ' '],
        ['0', '1', ' ', '1', '0', '2', ' ', ' '],
        ['0', '1', '1', '1', '0', '2', ' ', ' '],
        ['0', '0', '0', '1', '1', '3', ' ', ' '],
        ['0', '0', '0', '1', ' ', ' ', ' ', ' '],
    ]

    ms.uncover(5, 4)
    assert ms.score == 33
    assert ms.status == [
        ['0', '0', '0', '0', '0', '1', ' ', ' '],
        ['0', '1', '1', '1', '0', '1', ' ', ' '],
        ['0', '1', ' ', '1', '0', '2', ' ', ' '],
        ['0', '1', '1', '1', '0', '2', ' ', ' '],
        ['0', '0', '0', '1', '1', '3', ' ', ' '],
        ['0', '0', '0', '1', ' ', ' ', ' ', ' '],
    ]

    ms.uncover(4, 5)
    assert ms.score == 23
    assert ms.status == [
        ['0', '0', '0', '0', '0', '1', ' ', ' '],
        ['0', '1', '1', '1', '0', '1', ' ', ' '],
        ['0', '1', ' ', '1', '0', '2', ' ', ' '],
        ['0', '1', '1', '1', '0', '2', ' ', ' '],
        ['0', '0', '0', 'X', 'X', 'X', ' ', ' '],
        ['0', '0', '0', 'X', '*', 'X', ' ', ' '],
    ]

    ms.uncover(5, 5)
    assert ms.score == 23
    assert ms.status == [
        ['0', '0', '0', '0', '0', '1', ' ', ' '],
        ['0', '1', '1', '1', '0', '1', ' ', ' '],
        ['0', '1', ' ', '1', '0', '2', ' ', ' '],
        ['0', '1', '1', '1', '0', '2', ' ', ' '],
        ['0', '0', '0', 'X', 'X', 'X', ' ', ' '],
        ['0', '0', '0', 'X', '*', 'X', ' ', ' '],
    ]

    ms.uncover(6, 3)
    assert ms.score == -7
    assert ms.status == [
        ['0', '0', '0', '0', '0', '1', ' ', ' '],
        ['0', '1', '1', 'X', 'X', 'X', '*', 'X'],
        ['0', '1', ' ', 'X', 'X', 'X', 'X', 'X'],
        ['0', '1', '1', 'X', 'X', 'X', '*', 'X'],
        ['0', '0', '0', 'X', 'X', 'X', '*', 'X'],
        ['0', '0', '0', 'X', '*', 'X', 'X', 'X'],
    ]

    assert mines == {(2, 2): 5, (4, 5): 1, (6, 1): 0, (6, 3): 1, (6, 4): 3}


if __name__ == '__main__':
    main()
