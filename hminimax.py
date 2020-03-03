from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module import util


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
        self._MAXDEPTH = 1

    def _make_node_state(self, gameState):

        return hash((hash(gameState.getPacmanPosition()),
                     hash(gameState.getFood()),
                     hash(gameState.getGhostPosition(1))
                     ))

    def _terminal_test(self, gameState, depth) -> bool:
        # leaf node or end of game
        return gameState.isWin() or gameState.isLose() or depth == 0

    def _evalFct(self, gameState) -> int:
        pacPos = gameState.getPacmanPosition()
        foodList = gameState.getFood().asList()
        score = gameState.getScore()
        algo = LeeAlgo(gameState)

        if len(foodList) == 0:
            return score

        dist = algo.minMazeDistance(pacPos, foodList)
        return score - dist

    def _evalFct2(self, gameState) -> float:
        algo = LeeAlgo(gameState)
        pacPos = gameState.getPacmanPosition()
        # ghostPos = gameState.getGhostPosition(1)
        foodList = gameState.getFood().asList()
        score = gameState.getScore()
        offset = 2000

        # a) win factor
        if gameState.isWin():
            return score + 100 + offset

        # b) lose factor:
        # elif gameState.isLose():
        #     return score - 100 + offset # 4000

        # c) distance to food factor
        minFoodDist = algo.minMazeDistance(pacPos, foodList)
        score -= minFoodDist * 1.5

        # d) number food left factor:
        if len(foodList) > 0:
            score += ((1 / len(foodList)) * 100)

        # e) distance to ghost factor:
        # if util.manhattanDistance(pacPos, ghostPos) < 2:
        #     # runaway:
        #     score -= 20
        return score + offset

    # ------------------------------------------------------------------------

    def _max_value(self, gameState, depth) -> float:

        if self._terminal_test(gameState, depth):
            return self._evalFct(gameState)

        v = float("-inf")

        for (succGameState, succAction) in \
                gameState.generatePacmanSuccessors():

            succNodeState = self._make_node_state(succGameState)

            if succNodeState in self._visited and self._associatedScore[
                    succNodeState] >= succGameState.getScore():
                score = float("-inf")

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

    def _min_value(self, gameState, depth) -> float:

        if self._terminal_test(gameState, depth):
            return self._evalFct(gameState)

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
                self._associatedScore.clear()

                succNodeState = self._make_node_state(succGameState)
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

    def _isValid(self, i, j, x, y) -> bool:
        return (i > 0) and (i < self._M) and (j > 0) and (j < self._N) and (
                self._maze[x][y] is False) and (self._visited[i][j] is False)

    def _reset(self) -> None:
        self._visited = [[False for y in range(
            self._N)] for x in range(self._M)]
        self._fringe = util.Queue()
        self._minDist.clear()

    def _yToi(self, y) -> int:
        return self._M - 1 - y

    def _xToj(self, x) -> int:
        return x

    def minMazeDistance(self, pacman, food) -> int:
        food2DiscoverInit = len(food)
        food2Discover = len(food)

        node = Node(pacman[0], pacman[1], 0)
        self._fringe.push(node)

        for foodPos in food:
            self._minDist[foodPos] = float("inf")

        while not self._fringe.isEmpty():
            # speed up, useless to explore all the food in state space
            if food2Discover < food2DiscoverInit/1.5:
                break
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
            minDist = min(minDist, self._minDist[f])
        self._reset()
        return minDist
