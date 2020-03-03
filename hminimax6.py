# Complete this class for all parts of the project

from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module import util
from pacman_module import layout
from pacman_module import pacman as doc
import copy
import numpy as np


def terminal_test(gameState, depth)->bool:
    # leaf node or end of game
    return gameState.isWin() or gameState.isLose() or depth == 0


def make_node_state(gameState):

    return hash((hash(gameState.getPacmanPosition()),
            hash(gameState.getFood()),
            hash(gameState.getGhostPosition(1))
            ))

class PacmanAgent(Agent):

    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args

        # Stores the already explored nodes.
        # Set because hash functions are faster to retrieve an element (O(1))
        self._visited = set()
        self._associatedScore = {}
        self._depth = 0
        self._MAXDEPTH = 5
        self._time = 3

    # UTILITY FUNCTION
    def _evalFct(self, gameState)->float:
        return gameState.getScore()

    # BERKELEY 1
    def _evalFct2(self, gameState)->float:

        # Init
        pacPos = gameState.getPacmanPosition()
        foodList = gameState.getFood().asList()
        ghostPos = gameState.getGhostPositions()[0]
        score = gameState.getScore()

        def distClosestFood(pos, foodList):
            if len(foodList) == 0:
                return 1
            dist = float("+inf")
            for foodPos in foodList:
                dist = min(dist, util.manhattanDistance(pos, foodPos))
            return dist

        def dist2Ghost(pos, ghostPosition):
            return util.manhattanDistance(pos, ghostPosition)

        if gameState.isWin():
            return score + 1000
        if len(foodList) > 0:
            score = score + ((1/len(foodList)) * 200)

        if dist2Ghost(pacPos, ghostPos) < 2:
            score = -10000

        # subtract the distance to the closest food
        score = score - distClosestFood(pacPos, foodList)

        return score

    # BERKELEY
    def _evalFct4(self, gameState):
        try:
            newPos = gameState.getPacmanPosition()
            newFood = gameState.getFood().asList()
            newGhostStates = gameState.getGhostStates()

            # returns the distance to the closest food (manhatten distance)
            def distClose(pos, foodList):
                dist = float("inf")
                for foodPos in foodList:
                    dist = min(dist, util.manhattanDistance(pos, foodPos))
                return dist

            # just addes the game score
            score = gameState.getScore()
            if gameState.isWin():
                return 1000 + score

            # addes  1/food-count multiplied by 100 to the score if there is food left, if not returns 1000 for a win
            if len(newFood) > 0:
                score += ((1 / len(newFood) * 200))
            # if the ghost isn't scared run away, if it is go get em
            for i in range(len(newGhostStates)):
                ghostPos = newGhostStates[i].getPosition()

                if newPos == (ghostPos[0] - 1, ghostPos[1]):
                    score = -10000
                elif newPos == (ghostPos[0] + 1, ghostPos[1]):
                    score = -10000
                elif newPos == (ghostPos[0], ghostPos[1] - 1):
                    score = -10000
                elif newPos == (ghostPos[0], ghostPos[1] + 1):
                    score = -10000
                else:
                    if (abs(newPos[0] - ghostPos[0]) + abs(newPos[1] -
                                                           ghostPos[1])) == 0:
                        score = score + ((1 / 1) * 100)
                    else:
                        score = score + ((1 / (abs(newPos[0] - ghostPos[0]) +
                                             abs(
                            newPos[1] - ghostPos[1]))) * 100)

            # subtract the distance to the closest food
            score -= distClose(newPos, newFood)

            return score
        except Exception as e:
            print("Erreur ligne 191")
            print(e)

    # RETURN THE MANHATAN DISTANCE
    def _evalFct5(self, gameState):
        # Commence bien contre smarty

        pacPos = gameState.getPacmanPosition()
        foodList = gameState.getFood().asList()
        ghostPos = gameState.getGhostPositions()[0]
        score = gameState.getScore()

        if len(foodList) == 0:
            return 1
        dist = float("+inf")
        for foodPos in foodList:
            dist = min(dist, util.manhattanDistance(pacPos, foodPos))
        return score - dist

    # OLIVIER
    # La plus lente
    def _evalFct6(self, gameState):
        try:
            algo = LeeAlgo(gameState)
            pacPos = gameState.getPacmanPosition()
            ghostPos = gameState.getGhostPosition(1)
            food = gameState.getFood().asList()
            score = gameState.getScore()

            # a) win factor
            if gameState.isWin():
                score += 4000 #1000

            # b) lose factor:
            if gameState.isLose():
                score -= 3000 # 4000

            # c) distance to food factor
            minFoodDist = algo.minMazeDistance(pacPos, food)
            score -= minFoodDist * 40 # 30

            # d) number food left factor:
            if len(food) > 0:
                score += ((1 / len(food)) * 3000) # 300
            # else:
            #     score += 100

            # e) distance to ghost factor:
            # if util.manhattanDistance(pacPos, ghostPos) < 2:
            #     # runaway:
            #     score -= 20 # 800

            return score
        except Exception as e:
            print("Error is in the utilFct6: {}".format(e))
            return 0

    # OLIVIER: return real distance to food
    def _evalFct7(self, gameState):
        # démarre correctement sur dumby mais n'arrive pas à aller chercher
        # les 3 dernières

        # Fonctionnait sur dumby mais des fois boucle infinie. Opti pour
        # smarty la très grosse majorité du temps mais suscide sur large.
        # Greedy pas opti
        try:
            pacPos = gameState.getPacmanPosition()
            foodList = gameState.getFood().asList()
            ghostPos = gameState.getGhostPositions()[0]
            score = gameState.getScore()
            algo = LeeAlgo(gameState)

            if len(foodList) == 0 or gameState.isLose():# or gameState.isLose()
                return score

            dist = algo.minMazeDistance(pacPos, foodList)
            return score - dist

        except Exception as e:
            print("Error is in the utilFct6: {}".format(e))
            return 0

    # OLIVIER MANHATAN+
    def _evalFct8(self, gameState):
        # dist manhatan à la food
        # nbre de food restante
        # manhatan distance au ghost
        pacPos = gameState.getPacmanPosition()
        foodList = gameState.getFood().asList()
        ghostPos = gameState.getGhostPositions()[0]
        score = gameState.getScore()

        # a) distance to food
        distFood = float("+inf")
        for foodPos in foodList:
            distFood = min(distFood, util.manhattanDistance(pacPos, foodPos))

        # b) nb food left
        foodLeft = len(foodList)
        if foodLeft > 0:
            foodFactor = (1/foodLeft) * 100
        else:
            foodFactor = 100

        # c) ghost factor
        safeDist = util.manhattanDistance(pacPos, ghostPos)

        # d) lose factor
        loseFactor, winFactor = 0, 0
        if gameState.isLose():
            loseFactor = 150
        elif gameState.isWin():
            winFactor = 150

        return foodFactor - distFood * 8 + safeDist - loseFactor + winFactor



    # ------------------------------------------------------------------------

    def _max_value(self, gameState, depth):

        if terminal_test(gameState, depth):
            return self._evalFct8(gameState)

        v = float("-inf")

        for (succGameState, succAction) in \
                gameState.generatePacmanSuccessors():

            succNodeState = make_node_state(succGameState)

            if succNodeState in self._visited and self._associatedScore[
                    succNodeState] >= succGameState.getScore():
                score = float("-inf") # score=

            else:
                self._visited.add(succNodeState)
                self._associatedScore[succNodeState] = succGameState.getScore()
                score = self._min_value(succGameState, depth)

            v = max(v, score)

        if v == float("-inf"):
            # All sates have already been visited -> sub-tree should be ignored
            return float("+inf")
        return v

    # ------------------------------------------------------------------------

    def _min_value(self, gameState, depth):

        if terminal_test(gameState, depth):
            return self._evalFct8(gameState)

        v = float("+inf")

        for (succGameState, succAction) in \
                gameState.generateGhostSuccessors(1):


            score = self._max_value(succGameState, depth - 1)

            v = min(v, score)

        if v == float("+inf"):
            # All sates have already been visited -> sub-tree should be ignored
            return float("-inf")
        return v

    # ------------------------------------------------------------------------

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
        depth = self._MAXDEPTH

        try:
            if state.getNumAgents() - 1 != 1:
                raise Exception("One ghost is expected: not more not "
                                "less !")

            v = float("-inf")
            bestMove = Directions.STOP

            for (succGameState, succAction) in \
                    state.generatePacmanSuccessors():

                self._visited.clear()
                succNodeState = make_node_state(succGameState)
                self._visited.add(succNodeState)
                self._associatedScore[succNodeState] = succGameState.getScore()

                score = self._min_value(succGameState, depth)

                v = max(v, score)
                bestMove = succAction if v == score else bestMove

            return bestMove

        except Exception as e:
            print(e)


class Node:
    def __init__(self, x, y, dist2Root):
        self.x = x
        self.y = y
        self.distToRoot = dist2Root


class LeeAlgo:
    def __init__(self, gameState):
        self._fringe = util.Queue()
        self._maze = gameState.getWalls()
        self._M, self._N = self._maze.height, self._maze.width
        self._visited = [[False for y in range(
            self._N)] for x in range(self._M)]
        self._minDist = {}
        self._row, self._col = (-1, 0, 0, 1), (0, -1, 1, 0)

    def _isValid(self, i, j, x, y):
        return (i > 0) and (i < self._M) and (j > 0) and (j < self._N) and (
                self._maze[x][y] is False) and (self._visited[i][j] is False)

    def _reset(self):
        self._visited = [[False for y in range(
            self._N)] for x in range(self._M)]
        self._fringe = util.Queue()
        self._minDist.clear()

    def _yToi(self, y):
        return self._M - 1 - y

    def _xToj(self, x):
        return x

    def minMazeDistance(self, pacman, food):
        food2Discover = len(food)

        node = Node(pacman[0],pacman[1], 0)
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
                    break

            for mov in range(4):
                i = self._yToi(node.y)
                j = self._xToj(node.x)

                newX = node.x + self._row[mov]
                newY = node.y + self._col[mov]

                if self._isValid(self._yToi(newY), self._xToj(newX), newX,
                                 newY):
                    self._visited[i][j] = True
                    self._fringe.push(Node(newX, newY, dist + 1))

        minDist = float("inf")
        for f in food:
            tmp = self._minDist[f]
            minDist = min(minDist, self._minDist[f])
        self._reset()
        return minDist



