import random

from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.graphicsUtils import keys_waiting, keys_pressed
from pacman_module import util
import numpy as np


class PacmanAgent(Agent):
    """
    An agent controlled by the keyboard.
    """
    # NOTE: Arrow keys also work.
    WEST_KEY = 'j'
    EAST_KEY = 'l'
    NORTH_KEY = 'i'
    SOUTH_KEY = 'k'

    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.lastMove = Directions.STOP
        self.keys = []

    def get_action(self, state):
        """
        Given a pacman game state, returns a legal move.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Return:
        -------
        - A legal move as defined in `game.Directions`.
        """

        keys = keys_waiting() + keys_pressed()
        if keys != []:
            self.keys = keys

        legal = state.getLegalActions(0)
        move = self._get_move(legal)

        if move == Directions.STOP:
            # Try to move in the same direction as before
            if self.lastMove in legal:
                move = self.lastMove

        if move not in legal:
            move = random.choice(legal)

        self.lastMove = move
        test = LeeAlgo(state)
        print(test.minMazeDistance(state.getPacmanPosition(), state.getFood(

        ).asList()))
        return move

    def _get_move(self, legal):
        move = Directions.STOP
        if ((self.WEST_KEY in self.keys or 'Left' in self.keys) and
                Directions.WEST in legal):
            move = Directions.WEST
        if ((self.EAST_KEY in self.keys or 'Right' in self.keys) and
                Directions.EAST in legal):
            move = Directions.EAST
        if ((self.NORTH_KEY in self.keys or 'Up' in self.keys) and
                Directions.NORTH in legal):
            move = Directions.NORTH
        if ((self.SOUTH_KEY in self.keys or 'Down' in self.keys) and
                Directions.SOUTH in legal):
            move = Directions.SOUTH
        return move

    def _on_press(self, key, mod):
        try:
            self.pressedKey = chr(key)
        except Exception:
            pass

    def _on_release(self, key, mod):
        try:
            self.pressedKey = self.lastMove
        except Exception:
            pass


class Node:

    def __init__(self, x, y, distToRoot):
        self.x = x
        self.y = y
        self.distToRoot = distToRoot

class LeeAlgo:
    def __init__(self, gameState):
        self._fringe = util.Queue()
        self._maze = gameState.getWalls()
        self._M = self._maze.height
        self._N = self._maze.width
        self._visited = np.zeros((self._M, self._N), dtype=bool)
        self._minDist = {}

        self._row = (-1, 0, 0, 1)
        self._col = (0, -1, 1, 0)

    def _isValid(self, row , col):
        return (row >= 0) and (row < self._M) and (col >= 0) and ( col <
                                                                   self._N) \
        and (self._maze[row][col] == False) and (not self._visited[row][col])

    def _reset(self):
        self._visited = np.zeros((self._M, self._N), dtype=bool)
        self._fringe = util.Queue()
        # self._foodExplored.clear()
        self._minDist.clear()

    def minMazeDistance(self, pacman, food):

        x1, y1 = pacman[0], pacman[1]
        food2Discover = len(food)

        node = Node(x1, y1, 0)
        self._fringe.push(node)

        for foodPos in food:
            self._minDist[foodPos] = float("inf")

        while not self._fringe.isEmpty():
            node = self._fringe.pop()
            pos = (node.x, node.y)
            dist = node.distToRoot

            # If a food is discovered:
            if pos in food:
                self._minDist[pos] = dist
                food2Discover -= 1
                if food2Discover == 0:
                    # print("ok ligne 145")
                    break
                else:
                    continue

            for mov in range(4):
                # check if it is possible to go to position
                if self._isValid(node.x + self._row[mov], node.y + self._col[
                    mov]):
                    self._visited[node.x + self._row[mov]][node.y + self._col[
                        mov]] = True
                    newNode = Node(node.x + self._row[mov], node.y + self._col[
                        mov], dist + 1)
                    self._fringe.push(newNode)

        minDist = float("inf")
        for aFood in food:
            tmp = self._minDist[aFood]
            minDist = min(minDist, self._minDist[aFood])
            print("minDist = {} pour food = {}".format(tmp, aFood))
        self._reset()
        return minDist


    def mazeDistance(self, pos1, pos2):
        x1,y1 = pos1[0], pos1[1]
        x2,y2 = pos2[0], pos2[1]

        node = Node(x1, y1, 0)
        self._fringe.push(node)

        minDist = float("inf")

        while not self._fringe.isEmpty():
            node = self._fringe.pop()
            dist = node.distToRoot

            # destination found
            if node.x == x2 and node.y == y2:
                minDist = dist
                break

            for mov in range(4):
                # check if it is possible to go to position
                if self._isValid(node.x + self._row[mov], node.y+self._col[
                        mov]):

                    self._visited[node.x+self._row[mov]][node.y+self._col[
                        mov]] = True
                    newNode = Node(node.x+self._row[mov], node.y+self._col[
                        mov], dist+1)
                    self._fringe.push(newNode)
        if minDist != float("inf"):
            self._reset()
            return minDist

        else:
            print("Destination can't be reached from src")
            self._reset()
            return -1
