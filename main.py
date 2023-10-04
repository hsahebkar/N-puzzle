import pickle
import numpy as np
import matplotlib.pyplot as plt

from Lib import Tree
from tqdm import tqdm
from random import choice
from matplotlib.animation import FuncAnimation


class Npuzzle:
    def __init__(self, size: tuple, randomize: int):
        self.size = size
        self.MaxVal = self.size[0] * self.size[1]
        self.Spot = (self.size[0] - 1, self.size[1] - 1)
        self.Init_Board = None
        self.board = self.create_init_board(randomize)
        self.Board_list = Tree(self.board, self.Spot, self.Init_Board)

    def create_init_board(self, shuffle: int):
        print("Start Shuffling ...")
        board = np.arange(1, self.MaxVal + 1).reshape(self.size)
        board[self.Spot[0], self.Spot[1]] = 0

        self.Init_Board = np.arange(1, self.MaxVal + 1).reshape(self.size)
        self.Init_Board[self.Spot[0], self.Spot[1]] = 0

        if shuffle == 0:
            return board
        for _ in tqdm(range(shuffle)):
            sX, sY = self.Spot
            rX, rY = choice([(1, 0), (0, 1), (-1, 0), (0, -1)])
            new_point = sX + rX, sY + rY
            if 0 <= new_point[0] < self.size[0] and 0 <= new_point[1] < self.size[1]:
                board[self.Spot], board[new_point] = board[new_point], board[self.Spot]
                self.Spot = new_point
        return board

    @staticmethod
    def Plot_board(Boards: list[np.ndarray], Heuristics: list[int]):
        fig, ax = plt.subplots(1, 4)
        size = Boards[0].shape

        print(Boards[0], Boards[-1], sep="\n")

        ax[2].imshow(Boards[0])
        ax[3].imshow(Boards[-1])

        for i in range(size[0]):
            for j in range(size[1]):
                ax[2].text(j, i, str(Boards[0][i][j]), va='center', ha='center', fontsize=14)

        for i in range(size[0]):
            for j in range(size[1]):
                ax[3].text(j, i, str(Boards[-1][i][j]), va='center', ha='center', fontsize=14)

        ax[1].plot([i for i in range(len(Heuristics))], Heuristics, '--')
        heatmap = ax[0].matshow(Boards[0], cmap='viridis')
        annotations = []

        def update(frame):
            heatmap.set_data(Boards[frame])

            for ann in annotations:
                ann.remove()
            annotations.clear()

            for i in range(size[0]):
                for j in range(size[1]):
                    text = ax[0].text(j, i, str(Boards[frame][i][j]), va='center', ha='center', fontsize=14)
                    annotations.append(text)
            return [heatmap]

        ani = FuncAnimation(fig, update, frames=len(Boards), interval=500, repeat=True, repeat_delay=5000)
        plt.show()

    def __call__(self):
        self.Board_list()
        Boards, Heuristics = self.Board_list.Generate_Path()
        self.Plot_board(Boards, Heuristics)


if __name__ == '__main__':
    try:
        game = Npuzzle(size=(3, 3), randomize=1000)
        game()
    except KeyboardInterrupt:
        exit(0)
