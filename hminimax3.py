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

    return hash((hash(gameState.getPacmanPosition()),
            hash(gameState.getFood()),
            hash(gameState.getGhostPosition(1))
            ))
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
        self._associatedScore = {}
        self._depth = 0
        self._MAXDEPTH = 4

    def _evalFct(self, gameState)->float:
        return gameState.getScore()

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

    def _evalFct3(self, gameState)->float:

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
            a = distClosestFood(pacPos, currFoodList)
            if a == 0:
                a = 1
            if nFoodLeft == 0:
                b = 1
            else:
                b = nFoodLeft
            return 100.0/a + 1000/b

        def getWinBonus():
            return 100000  # float("+inf")

        dist2Ghost = dist2Ghost(pacPos, ghostPos)

        return score + getWinBonus() + getFoodBonus() + getGhostMalus()

    def _evalFct4(self, gameState):
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

    def _evalFct5(self, gameState):

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

    def _evalFct6(self, gameState):

        if gameState.isLose() or gameState.isWin():
            return gameState.getScore()

        minDistToFood = float("+inf")
        # for each new point to reach
        for food in gameState.getFood().asList():

            print("going through the food list")

            children = util.Queue()
            visited = []
            successors = gameState.generatePacmanSuccessors()

            # we push all successors in a queue, with 1 for the distance
            #  since they are one move apart from the initial position
            for successor in successors:
                print("added an original child")
                succState = successor[0]
                children.push((succState, 1))
                # we remember what positions have already been explored
                visited.append(succState.getPacmanPosition())

            while not children.isEmpty():
                (childState, distance) = children.pop()
                visited.append(childState.getPacmanPosition())
                print("new child ")
                # if this pacManPosition is the same as the food one
                # we see if the distance between them is the minimal one
                # to date, if yes, we update minDistToFood
                if food == childState.getPacmanPosition():
                    print("found a food !!!!!!!!!!!!!!")
                    minDistToFood = min(distance, minDistToFood)
                    break
                else:
                    for subChild in childState.generatePacmanSuccessors():
                        # the distance from the origin is one more than the one
                        # of the parent
                        nextState = subChild[0]
                        if nextState.getPacmanPosition() not in visited:
                            print("pushed an unvisited child")
                            children.push((nextState, distance+1))
            print("out of the queue")
        print("BEST DIST IS : {}".format(minDistToFood))

        return - minDistToFood + gameState.getScore()








    # ------------------------------------------------------------------------

    def _max_value(self, gameState, depth):

        if terminal_test(gameState, depth):
            return self._evalFct6(gameState)

        v = float("-inf")

        for (succGameState, succAction) in \
                gameState.generatePacmanSuccessors():

            succNodeState = make_node_state(succGameState)

            # [?] Passer en argument ? -> minimax 5 ?
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
            return self._evalFct6(gameState)

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

                print(succGameState)
                print(self._evalFct6(succGameState))

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
