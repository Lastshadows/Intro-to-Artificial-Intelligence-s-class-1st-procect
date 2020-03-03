# Complete this class for all parts of the project

from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module import util
from pacman_module import layout
from pacman_module import pacman as doc
import copy


def terminal_test(gameState, depth)->bool:
    # leaf node or end of game
    return gameState.isWin() or gameState.isLose() or depth == 0


def make_node_state(gameState):

    return (hash(gameState.getPacmanPosition()),
            hash(gameState.getFood()),
            hash(gameState.getGhostPosition(1))
            )
    # return (gameState.getPacmanPosition(),gameState.getFood(),gameState.getGhostPosition(1)
    #             )

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
        self._depth = 0
        self._winStates = []
        self._ncall = 0

        self._MAXDEPTH = 4

    def _utilFct(self, gameState, depth)->float:
        # if gameState.isWin():
        #     return 1
        # else:
        #     return -1

        if gameState.isWin():
            self._winStates.append(gameState)
            print("WIN -> {}".format(gameState.getScore()))
            return gameState.getScore()
        if gameState.isLose():

            print("LOOSE")
            return gameState.getScore()
        if depth == 0:
            print("DEPTH REACHED")
            return float(gameState.getScore())

    def _evalFct(self, gameState)->float:

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

    def _evalFct2(self, gameState)->float:

        # Init
        pacPos = gameState.getPacmanPosition()
        currFood = gameState.getFood()
        currFoodList = gameState.getFood().asList()
        ghostPos = gameState.getGhostPositions()[0]
        nFoodLeft = float(len(currFoodList))
        score = gameState.getScore()
        foodBonus, ghostMalus = 0, 0

        def distClosestFood(pos, foodList):
            if len(foodList) == 0:
                return 1
            dist = float("+inf")
            for foodPos in foodList:
                dist = min(dist, util.manhattanDistance(pos, foodPos))
            return dist

        def dist2Ghost(pos, ghostPosition):
            return util.manhattanDistance(pos, ghostPosition)

        def getGhostMalus():
            if dist2Ghost < 1:
                # return -100000
                return float("-inf")
            elif dist2Ghost < 2:
                return -1000
            else: # safe
                return + 100

        def getFoodBonus():
            return 100.0/distClosestFood(pacPos, currFoodList) + 1000/nFoodLeft

        def getWinBonus():
            return 100000  # float("+inf")

        dist2Ghost = dist2Ghost(pacPos, ghostPos)

        return score + getWinBonus() + getFoodBonus() + getGhostMalus()

    def _evalFct3(self, gameState):
        try:
            newPos = gameState.getPacmanPosition()
            newFood = gameState.getFood()
            newGhostStates = gameState.getGhostStates()

            print("Alive 1")


            # returns the distance to the closest food (manhatten distance)
            def distClose(position, foodGrid):
                print("Alive 10, 25")
                gridInfo = foodGrid
                print("Alive 10,5")
                value = None

                for i, a in enumerate(foodGrid):
                    for j, b in enumerate(foodGrid[i]):
                        if foodGrid[i][j] is True:
                            dist = (
                            (abs(position[0] - i) + abs(position[1] - j)), (i, j))
                            if value is None:
                                value = dist
                            if dist[0] < value[0]:
                                value = dist
                print("Alive 11")
                if value == None:
                    print("Alive 12")
                    value = (0, position)
                print("Alive 13")
                return value

            # just addes the game score
            score = gameState.getScore()
            print("Alive 2")
            if gameState.isWin():
                return 1000 + score
            print("Alive 3")

            # addes  1/food-count multiplied by 100 to the score if there is food left, if not returns 1000 for a win
            if newFood.count() > 0:
                score += ((1 / newFood.count()) * 200)
            print("Alive 4")
            # if the ghost isn't scared run away, if it is go get em
            for i in range(len(newGhostStates)):
                ghostPos = newGhostStates[i].getPosition()
                print("Alive 5")

                if newPos == (ghostPos[0] - 1, ghostPos[1]):
                    print("Alive 6")
                    score = -10000
                elif newPos == (ghostPos[0] + 1, ghostPos[1]):
                    print("Alive 6")
                    score = -10000
                elif newPos == (ghostPos[0], ghostPos[1] - 1):
                    print("Alive 6")
                    score = -10000
                elif newPos == (ghostPos[0], ghostPos[1] + 1):
                    print("Alive 6")
                    score = -10000
                else:
                    print("Alive 7")
                    if (abs(newPos[0] - ghostPos[0]) + abs(newPos[1] -
                                                           ghostPos[1])) == 0:
                        score = score + ((1 / 1) * 100)
                        print("Alive 8")
                    else:
                        score = score + ((1 / (abs(newPos[0] - ghostPos[0]) +
                                             abs(
                            newPos[1] - ghostPos[1]))) * 100)
                        print("Alive 9")

            # subtract the distance to the closest food
            print("Alive 9,5")
            score -= distClose(newPos, newFood)[0]
            print("Alive 10")

            return score
        except Exception as e:
            print("Erreur ligne 191")
            print(e)

    def _evalFct4(self, gameState):

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


    # ------------------------------------------------------------------------
    def _max_value(self, gameState, depth)->(float, doc.GameState):

        if terminal_test(gameState, depth):
            return self._utilFct(gameState, depth)

        v = float("-inf")

        for (succGameState, succAction) in \
                gameState.generatePacmanSuccessors():

            succNodeState = hash(make_node_state(succGameState))

            # [?] Passer en argument ? -> minimax 5 ?
            if succNodeState in self._visited:
                score = float("-inf") # score=

            else:
                self._visited.add(succNodeState)
                score = self._min_value(succGameState, depth)

            v = max(v, score)

        if v == float("-inf"):
            # All sates have already been visited -> sub-tree should be ignored
            return float("+inf")
        return v

    # ------------------------------------------------------------------------
    def _min_value(self, gameState, depth)->(float, doc.GameState):

        self._depth += 1
        if terminal_test(gameState, depth):
            self._depth -= 1
            return self._utilFct(gameState, depth)

        v = float("+inf")

        for (succGameState, succAction) in \
                gameState.generateGhostSuccessors(1):

            succNodeState = hash(make_node_state(succGameState))

            if succNodeState in self._visited:
                score = float("+inf") # skip it to avoid loop
            else:
                self._visited.add(succNodeState)
                score = self._max_value(succGameState, depth - 1)

            v = min(v, score)
        self._depth -= 1

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
        self._ncall += 1
        self._winStates.clear()
        print("--------- [GET ACTION {}] ----------".format(self._ncall))
        try:
            if state.getNumAgents() - 1 != 1:
                raise Exception("One ghost is expected: not more not "
                                "less !")

            v = float("-inf")
            bestMove = Directions.STOP
            i=0
            for (succGameState, succAction) in \
                    state.generatePacmanSuccessors():
                i += 1
                # nodeState = hash(make_node_state(succGameState))

                # if nodeState in self._visited:
                #     print("already visited")
                #     score = float("-inf") # quasiment tt tombe dans le
                #     # visited et donc score->v est quasi tjrs = à -infinity
                #
                # else:
                #     print("Here")
                #     self._visited.add(nodeState)
                #     score = self._min_value(succGameState)
                print("[GameState {}]".format(i))
                self._visited.clear()
                score = self._min_value(succGameState, depth)
                print("[v]Before:v = {} and score = {}".format(v,score))  # ->
                # tous les v sont à -\infty
                v = max(v, score)

                print("[v]After:{}".format(v))  # -> tous les v sont à -\infty
                bestMove = succAction if v == score else bestMove
                print("---")

            print("=> For this called, used v = {}".format(v))
            for winningState in self._winStates:
                print(winningState)
            return bestMove

        except Exception as e:
            print(e)

# visited et renvoit +inf ou -inf si déjà présent ou non. Pas de depth