# Complete this class for all parts of the project

from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module import util
from pacman_module import layout
from pacman_module import pacman as doc
import copy


def terminal_test(gameState, depth)->bool:
    # leaf node or end of game

    if gameState.isWin():
        print("[terminal_test] Game is won !")

    if gameState.isLose():
        print("[terminal_test] Game is lost !")

    return depth == 0 or gameState.isWin() or gameState.isLose()


def make_node_state(gameState):
    # return (hash(gameState.getPacmanPosition()),
    #         hash(gameState.getFood()),
    #         hash(tuple(gameState.getGhostStates()))
    #         )
    return (hash(gameState.getPacmanPosition()),
            hash(gameState.getFood()),
            hash(tuple(gameState.getGhostPositions()))
            )


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

        self._MAXDEPTH = 4


    def _utilFct(self, gameState)->float:

        return float(gameState.getScore())

    # ------------------------------------------------------------------------
    def _max_value(self, gameState, depth)->(float, doc.GameState):

        if terminal_test(gameState, depth):
            print("/!\ [max_value] Terminal node reached !")
            print("depth : {}\n \n is Win ? {} \n \n is Lost ? : {} ".format(depth, gameState.isWin(), gameState.isLose()))
            return self._utilFct(gameState)

        v = float("-inf")
        bestMove = Directions.STOP

        for (succGameState, succAction) in \
                gameState.generatePacmanSuccessors():

            print("[max_value]Successor ({}):".format(succAction))
            #print(succGameState)

            succNodeState = hash(make_node_state(succGameState))

            # [?] Passer en argument ? -> minimax 5 ?
            if succNodeState in self._visited:
                print("[max_value] This state has already been visited -> "
                      "skip")
                continue

            #self._visited.add(succNodeState)

            score = self._min_value(succGameState, depth)

            v = max(v, score)
            # bestMove = succAction if v == score else bestMove

        # Everything already visited: avoid loop
        # if bestMove == Directions.STOP:
        #     print("[max_value] bestMove is STOP -> avoid loop")
        #     return float("+inf")

        # if depth == self._MAXDEPTH:
        #     return bestMove
        # else:
        return v

    # ------------------------------------------------------------------------
    def _min_value(self, gameState, depth)->(float, doc.GameState):

        if terminal_test(gameState, depth):
            print("[min_value] Terminal node reached /!/ ")
            return self._utilFct(gameState)

        v = float("+inf")
        bestMove = Directions.STOP

        for (succGameState, succAction) in \
                gameState.generateGhostSuccessors(1):

            print("[min_value]Successor ({}):".format(succAction))
            #print(succGameState)

            succNodeState = hash(make_node_state(succGameState))
            if succNodeState in self._visited:
                print("[min_value] This state has already been visited")
                continue

            score = self._max_value(succGameState, depth - 1)
            # copy.deepcopy()
            print("[min_value]End of call max_value: StateMax=")

            print("[min_value]vmax  = {}".format(score))
            print("[min_value]v  = {}".format(v))
            v = min(v, score)
            print("[min_value]now v  = {}".format(v))

                # bestMove = succAction if v == score else bestMove

        # Everything already visited: avoid loop
        # if bestMove == Directions.STOP:
        #     # because called by min_value, it should not be taken in the max(
        #     # v, min_value())
        #     print("[min_value] bestMove is STOP -> avoid loop")
        #     return float("-inf")

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

                score = self._min_value(succGameState, depth)

                v = max(v, score)
                bestMove = succAction if v == score else bestMove

            return bestMove

        except Exception as e:
            print(e)