# Complete this class for all parts of the project

from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module import util


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
        self._MAXDEPTH = 3
        self._time = 3

    # UTILITY FUNCTION => 3,75/9
    def _evalFct(self, gameState)->float:
        # small_adv: dumby, greedy, smarty gagne, opti
        # medium_adv:
        #   - dumby: commence bien mais boucle infinie ou bien gagne pas opti
        #   - greedy: gagne opti
        #   - smarty: suicidaire sur la fin mais a déjà gagné 1 fois opti
        # large_adv:
        #   - dumby: s'isole mur puis boucle infinie
        #   - greedy: commence bien (sauf la 1ère) puis suicide ou bien
        #               boucle infinie sur l'ilot
        #   - smarty: commence bien (sauf la 1ère) puis suicide
        return gameState.getScore()

    # RETURN THE MANHATAN DISTANCE => 4,3/9
    def _evalFct2(self, gameState):
        # small_adv: dumby, greedy, smarty gagne, opti
        # medium_adv:
        #   - dumby: gagne pas opti (revient à des états précédents)
        #   - greedy: gagne pas opti ou suicidaire sur la fin, opti 1 fois
        #   - smarty: suicidaire sur la fin mais a déjà gagné 1 fois opti
        # large_adv:
        #   - dumby: gagne pas opti
        #   - greedy: commence bien (sauf la 1ère) puis suicide ou bien
        #               suicide par manque de prévoyance
        #   - smarty: commence bien (sauf la 1ère) puis suicide ou bien
            #           suicide par manque de prévoyance

        pacPos = gameState.getPacmanPosition()
        foodList = gameState.getFood().asList()
        ghostPos = gameState.getGhostPositions()[0]
        score = gameState.getScore()

        if len(foodList) == 0:
            return score
        dist = float("+inf")
        for foodPos in foodList:
            dist = min(dist, util.manhattanDistance(pacPos, foodPos))
        return score - dist

    # OLIVIER => 0/9
    # La plus lente
    # small_adv: perdent tous
    # medium_adv:
    #   - dumby: /
    #   - greedy: /
    #   - smarty: /
    # large_adv:
    #   - dumby: /
    #   - greedy: /
    #   - smarty: /
    def _evalFct3(self, gameState):
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

    # OLIVIER: return real distance to food => 5,5/9
    # Si elle est réglée en self._depth=3 !
    def _evalFct4(self, gameState):
        # méga-lent
        # small_adv: dumby, greedy, smarty gagne, opti
        # medium_adv:
        #   - dumby: pas opti mais gagne
        #   - greedy: gagne opti svt
        #   - smarty: gagne opti svt
        # large_adv: (n'arrive pas à terminer car trop lent une fois à dr.)
        #   - dumby: mouvements inutiles mais boucle infinie
        #   - greedy: suicidaire
        #   - smarty: suicidaire
        try:
            pacPos = gameState.getPacmanPosition()
            foodList = gameState.getFood().asList()
            ghostPos = gameState.getGhostPositions()[0]
            score = gameState.getScore()
            algo = LeeAlgo(gameState)

            if len(foodList) == 0:# or gameState.isLose()
                return score

            dist = algo.minMazeDistance(pacPos, foodList)
            return score - dist

        except Exception as e:
            print("Error is in the utilFct6: {}".format(e))
            return 0

    # OLIVIER MANHATAN+ => 0/9
    def _evalFct5(self, gameState):
        # small_adv: perdent tous
        # medium_adv:
        #   - dumby: /
        #   - greedy: /
        #   - smarty: /
        # large_adv:
        #   - dumby: /
        #   - greedy: /
        #   - smarty: /

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

    def _evalFct6(self, gameState):
        # depth = 3
        # small_adv: dumby, greedy, smarty gagne, opti
        # medium_adv:
        #   - dumby: boucle infinie
        #   - greedy: gagne pas opti ou suicidaire sur la fin, opti 1 fois
        #   - smarty: suicidaire sur la fin mais a déjà gagné 1 fois opti
        # large_adv:
        #   - dumby: gagne pas opti
        #   - greedy: commence bien (sauf la 1ère) puis suicide ou bien
        #               suicide par manque de prévoyance
        #   - smarty: commence bien (sauf la 1ère) puis suicide ou bien
            #           suicide par manque de prévoyance

        pacPos = gameState.getPacmanPosition()
        foodList = gameState.getFood().asList()
        ghostPos = gameState.getGhostPositions()[0]
        score = gameState.getScore()

        if len(foodList) == 0:
            return score
        dist = float("+inf")
        for foodPos in foodList:
            dist = min(dist, util.manhattanDistance(pacPos, foodPos))
        print(dist)
        return score - dist



    # ------------------------------------------------------------------------

    def _max_value(self, gameState, depth):

        if terminal_test(gameState, depth):
            return self._evalFct4(gameState)

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
            return self._evalFct4(gameState)

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
        food2DiscoverInit = len(food)
        food2Discover = len(food)

        node = Node(pacman[0],pacman[1], 0)
        self._fringe.push(node)

        for foodPos in food:
            self._minDist[foodPos] = float("inf")

        while not self._fringe.isEmpty():
            # speed up
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
            tmp = self._minDist[f]
            minDist = min(minDist, self._minDist[f])
        self._reset()
        return minDist



