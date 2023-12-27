import random
import tkinter as tk
import game_logic as student

# game parameters; feel free to change them
WIDTH = 30
HEIGHT = 16
MINES = 50
MAX_FORCE = 3

CELL_SIZE = 20
NUM_FONT = ('system', 16)
BOTTOM = 150
SCORE_FONT = ('system', 12)
BACKGROUND = '#d9d9d9'

TILE_COLOUR = {' ': '#008000', 'X': '#292929',
               '*': '#800000', "F": '#ffff00'}

FLAG = "#000000"
NUM_COLOURS = [
    BACKGROUND,
    '#0000ff',
    '#008100',
    '#ff1300',
    '#000083',
    '#810500',
    '#2a9494',
    '#000000',
    '#808080',
    FLAG,
]


class Game:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.canvas = tk.Canvas(width=WIDTH * CELL_SIZE + 1,
                                height=HEIGHT * CELL_SIZE + BOTTOM)
        self.canvas.pack()

        self.reset()

        self.canvas.bind("<Button-3>", self.flag)
        self.canvas.bind("<Button-1>", self.click)
        self.canvas.bind_all("r", lambda _: self.reset())
        self.canvas.bind_all("q", lambda _: self.root.destroy())

    def reset(self) -> None:
        positions = [(x, y) for x in range(WIDTH) for y in range(HEIGHT)]

        mines = {pos: random.randint(0, MAX_FORCE)
                 for pos in random.sample(positions, MINES)}

        self.ms = student.Minesweeper(WIDTH, HEIGHT, mines)

        self.refresh()

    def refresh(self) -> None:
        self.canvas.delete('all')
        uncovered = 0
        exploded = 0
        flagged = 0

        for y, row in enumerate(self.ms.status):
            for x, tile in enumerate(row):
                if tile == ' ':
                    uncovered += 1
                elif tile == '*':
                    exploded += 1
                elif tile == "F":
                    flagged += 1


                cy = y * CELL_SIZE + 1
                cx = x * CELL_SIZE + 1
                self.canvas.create_rectangle(
                    cx, cy, cx + CELL_SIZE, cy + CELL_SIZE,
                    fill=TILE_COLOUR.get(tile, BACKGROUND)
                )
                if tile.isdecimal():
                    self.canvas.create_text(
                        cx + CELL_SIZE // 2, cy + CELL_SIZE // 2,
                        text=tile, font=NUM_FONT,
                        fill=NUM_COLOURS[int(tile)]
                    )
                if tile == "F":
                    self.canvas.create_text(
                        cx + CELL_SIZE // 2, cy + CELL_SIZE // 2,
                        text=tile, font=NUM_FONT,
#                         fill=NUM_COLOURS[-1],
                        fill=TILE_COLOUR.get(tile, BACKGROUND)
                    )

        self.canvas.create_text(
            1 + WIDTH // 2 * CELL_SIZE,
            1 + HEIGHT * CELL_SIZE + BOTTOM // 3,
            text=f"Score: {self.ms.score}\n" + (
                f"Mines remaining: {MINES - exploded - flagged}\n"
                f"Mines flagged: {flagged}\n"
                f"Uncovered tiles: {uncovered}\n"
                if exploded + uncovered + flagged > MINES else
                "Game over!\nPress r to restart or q to quit."
            ),
            font=SCORE_FONT
        )

    def click(self, event: tk.Event) -> None:
        x = event.x - 1
        y = event.y - 1
        if (x < 0 or x % CELL_SIZE == 0 or y < 0 or y % CELL_SIZE == 0 or
                y // CELL_SIZE >= HEIGHT):
            return

        self.ms.uncover(x // CELL_SIZE, y // CELL_SIZE)
        self.refresh()
    
    def flag(self, event: tk.Event) -> None:
        x = event.x - 1
        y = event.y - 1
        if (x < 0 or x % CELL_SIZE == 0 or y < 0 or y % CELL_SIZE == 0 or
                y // CELL_SIZE >= HEIGHT):
            return

        self.ms.flag(x // CELL_SIZE, y // CELL_SIZE)
        self.refresh()


def main() -> None:
    game = Game()
    game.root.mainloop()


if __name__ == '__main__':
    main()
