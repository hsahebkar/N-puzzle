import random
from typing import Iterator
from .Tools import Heuristic


Banned_move = {
    (1, 0): (-1, 0),
    (0, 1): (0, -1),
    (-1, 0): (1, 0),
    (0, -1): (0, 1)
}


class Node:
    def __init__(self, board, spot, depth, heuristic, Banned, pre=None):
        self._Pre: Node | None = pre
        self._Next = [Node, ...]
        self.board = board
        self.spot: tuple = spot
        self.depth = depth
        self.heuristic: float = heuristic
        self.searched = 0
        self.Banned = Banned

    def moves(self, x, y) -> Iterator[tuple]:
        """
        Generates possible moves (positions and banned move information) from a given position (x, y).

        Args:
            x (int): The x-coordinate of the current position.
            y (int): The y-coordinate of the current position.

        Yields:
            tuple: A tuple containing:
                - A new position (x', y') resulting from a possible move.
                - A tuple representing the banned move information. The banned move is the opposite of the current move.

        Note:
            The 'Banned' attribute should be set in the object to specify moves that are banned. The banned move for each generated
            move is the opposite of the current move. For example, if the current move is (1, 0), the banned move is (-1, 0).
        """
        for Mx, My in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            if (Mx, My) == self.Banned:
                continue
            yield (x + Mx, y + My), Banned_move[(Mx, My)]

    def possible_moves(self, board, spot):
        """
        Generates a list of possible boards resulting from valid moves of a piece on a given board.

        Args:
            - board (numpy.ndarray): The current board state represented as a 2D numpy array.
            - spot (tuple): The coordinates (x, y) of the piece to be moved.

        Returns:
            List[tuple]: A list of tuples, each containing:
                - A new board state after a valid move.
                - The destination coordinates of the moved piece.
                - Banned move information for the next move.

        Note:
            The 'Banned' attribute should be set in the object to specify moves that are banned. This function only considers
            valid moves within the bounds of the board.
        """
        sX, sY = spot
        size = board.shape
        Boards = []
        for PO, next_Banned in self.moves(sX, sY):
            new_board = board.copy()
            if 0 <= PO[0] < size[0] and 0 <= PO[1] < size[1]:
                new_board[spot], new_board[PO] = new_board[PO], new_board[spot]
                Boards.append((new_board, PO, next_Banned))
        return Boards

    def add_Next(self, node):
        self._Next.append(node)

    def set_pre(self, val):
        self._Pre = val

    @property
    def Next(self):
        return self._Next

    @property
    def Pre(self):
        return self._Pre


class Tree:
    def __init__(self, board, spot, Goal, Threshold=100):
        self.Threshold: int = Threshold
        self.Goal = Goal
        self.Placement = self.Generate_heuristic_table()
        self.Final: Node | None = None
        _, init_board_heuristic = Heuristic(board, Goal)
        Init_node = Node(board, spot, 0, init_board_heuristic, Banned=None, pre=None)
        self.Tail: Node | None = Init_node
        self.Boards_on_process: list[Node, ...] = [Init_node]
        self.DEPTH = []
        self.heuristics_total = 0
        self.plot_res = {}

    def Generate_heuristic_table(self) -> dict:
        """
        Generates a heuristic table mapping values in the 'Goal' matrix to their positions.

        This function creates a dictionary where keys are unique values found in the 'Goal' matrix, and values are tuples representing
        the (row, column) positions of those values within the matrix.

        Returns:
            dict: A dictionary where keys are values in the 'Goal' matrix and values are corresponding (row, column) positions.

        Note:
            The 'Goal' matrix must be defined in the object before calling this function.

        Example:
            If 'Goal' is a 2D matrix like this:
            [[1, 2],
             [3, 4]]

            The function will return:
            {1: (0, 0), 2: (0, 1), 3: (1, 0), 4: (1, 1)}
        """
        Placement = {}
        size = self.Goal.shape
        for i in range(size[0]):
            for j in range(size[1]):
                Placement[self.Goal[i, j]] = (i, j)
        return Placement

    def Generate_Path(self):
        """
        Generates a path by traversing the linked list of nodes from the 'Final' node to the root.

        This function starts from the 'Final' node and iterates through the linked list of nodes, extracting each board state and
        its corresponding heuristic value. It constructs two lists: one for board states and one for heuristics. The lists are
        ordered from the initial state to the final state.

        Returns:
            Tuple[list[np.ndarray], List[int]]: A tuple containing two lists:
                - A list of board states (2D matrices) representing the path from the initial state to the final state.
                - A list of heuristic values corresponding to each board state in the path.

        Note:
            The 'Final' node must be set in the object before calling this function. The linked list should be properly constructed
            to represent the path from the initial state to the final state.
        """
        Boards = []
        heuristics = []
        pointer = self.Final
        while pointer:
            board = pointer.board
            Boards.append(board)
            heuristics.append(pointer.heuristic)
            pointer = pointer.Pre

        return Boards[::-1], heuristics[::-1]

    def GDC(self):
        """
        Garbage Data Collector:
            this function remove the nodes with less than require point
        """
        avg = self.heuristics_total / len(self.Boards_on_process)
        print(f'{avg = }')
        tmp_Boards_on_process = []
        for node in self.Boards_on_process:
            if node.heuristic <= avg:
                tmp_Boards_on_process.append(node)
        self.Boards_on_process = tmp_Boards_on_process

    def Max_node(self):
        """
            Selects and returns the node with the highest heuristic value from the list of boards on process (self.Boards_on_process).
            This function first try to choose randomly with 0.2 percent chance otherwise it iterates through the list to find the node with the highest score value.
            "Lower heuristic -> higher score"
            Returns:
                Node: The selected node with the highest heuristic value.

            Note:
                This function modifies the internal state of the object by updating the `heuristics_total` and removing nodes from the `Boards_on_process` list.

        """
        # if len(self.Boards_on_process) > self.Threshold:
        #     self.GDC()
        if random.random() < 0.2:
            max_index = random.randint(0, len(self.Boards_on_process) - 1)
            max_node: Node = self.Boards_on_process[max_index]
            self.heuristics_total -= self.Boards_on_process[max_index].heuristic
            del self.Boards_on_process[max_index]
            return max_node

        max_node: Node = self.Boards_on_process[0]
        self.heuristics_total = max_node.heuristic
        max_index = 0
        Black_list = []
        for i, node in enumerate(self.Boards_on_process):
            # if node.searched > 1000:
            #     Black_list.append(i)
            #     continue
            self.heuristics_total += node.heuristic
            # if (node.heuristic < max_node.heuristic or
            #         (node.heuristic == max_node.heuristic and node.depth < max_node.depth)):
            if node.heuristic < max_node.heuristic:
                max_index = i
                max_node = node
            else:
                node.searched += 1

        self.heuristics_total -= self.Boards_on_process[max_index].heuristic

        Black_list.append(max_index)
        item_deleted = 0
        for del_index in Black_list:
            self.heuristics_total -= self.Boards_on_process[del_index - item_deleted].heuristic
            del self.Boards_on_process[del_index - item_deleted]
            item_deleted += 1

        return max_node

    def __call__(self):
        current_level = -1
        while self.Boards_on_process:
            node = self.Max_node()
            self.DEPTH.append(node.depth)
            if node.depth != current_level:
                current_level = node.depth
            print(f'Current Searching Depth: {current_level: >3} -> {len(self.Boards_on_process) = }')

            for subBoard, spot, next_Ban in node.possible_moves(node.board, node.spot):
                is_match, subBoard_Heuristic = Heuristic(subBoard, self.Goal)
                new_node = Node(subBoard, spot, node.depth + 1, subBoard_Heuristic, next_Ban, node)
                key = f'{node.depth}'
                if key not in self.plot_res:
                    self.plot_res[key] = []
                self.plot_res[key].append(subBoard_Heuristic)
                if is_match:
                    self.Final = new_node
                    del self.Boards_on_process
                    return
                node.add_Next(new_node)
                self.Boards_on_process.append(new_node)
