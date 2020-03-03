# Complete this class for all parts of the project

from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module import util
from pacman_module import layout
from pacman_module import pacman as doc
import copy


def terminal_test(gameState)->bool:
    # leaf node or end of game
    return gameState.isWin() or gameState.isLose()


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

    def _utilFct(self, gameState)->float:
        # if gameState.isWin():
        #     return 1
        # else:
        #     return -1

        if gameState.isWin():
            self._winStates.append(gameState)
            print("WIN -> {}".format(gameState.getScore()))
            return gameState.getScore()
        else:

            print("LOOSE")
            return gameState.getScore()


        # return float(gameState.getScore())

    # ------------------------------------------------------------------------
    def _max_value(self, gameState)->(float, doc.GameState):

        if terminal_test(gameState):
            return self._utilFct(gameState)

        v = float("-inf")

        for (succGameState, succAction) in \
                gameState.generatePacmanSuccessors():

            succNodeState = hash(make_node_state(succGameState))

            # [?] Passer en argument ? -> minimax 5 ?
            if succNodeState in self._visited:
                score = float("-inf") # score=

            else:
                self._visited.add(succNodeState)
                score = self._min_value(succGameState)

            v = max(v, score)

        if v == float("-inf"):
            # All sates have already been visited -> sub-tree should be ignored
            return float("+inf")
        return v

    # ------------------------------------------------------------------------
    def _min_value(self, gameState)->(float, doc.GameState):

        self._depth += 1
        if terminal_test(gameState):
            self._depth -= 1
            return self._utilFct(gameState)

        v = float("+inf")

        for (succGameState, succAction) in \
                gameState.generateGhostSuccessors(1):

            succNodeState = hash(make_node_state(succGameState))

            if succNodeState in self._visited:
                score = float("+inf") # skip it to avoid loop
            else:
                self._visited.add(succNodeState)
                score = self._max_value(succGameState)

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
                score = self._min_value(succGameState)
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