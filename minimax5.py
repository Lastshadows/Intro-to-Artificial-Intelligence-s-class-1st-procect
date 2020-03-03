

# Complete this class for all parts of the project

from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module import util
from pacman_module import layout
from pacman_module import pacman as doc
import copy


def terminal_test(gameState, depth)->bool:
    # leaf node or end of game
    return depth == 0 or gameState.isWin() or gameState.isLose()


def make_node_state(gameState):

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

        self._MAXDEPTH = 2


    def _utilFct(self, gameState)->float:

        return float(gameState.getScore())

    # ------------------------------------------------------------------------
    def _max_value(self, gameState, depth)->(float, doc.GameState):

        if terminal_test(gameState, depth):
            return self._utilFct(gameState)

        v = float("-inf")
        # bestMove = Directions.STOP

        for (succGameState, succAction) in \
                gameState.generatePacmanSuccessors():

            succNodeState = hash(make_node_state(succGameState))

            # [?] Passer en argument ? -> minimax 5 ?
            # if succNodeState in self._visited:
            #     continue

            # self._visited.add(succNodeState)

            score = self._min_value(succGameState, depth)

            v = max(v, score)
        return v

    # ------------------------------------------------------------------------
    def _min_value(self, gameState, depth)->(float, doc.GameState):

        if terminal_test(gameState, depth):
            return self._utilFct(gameState)

        v = float("+inf")
        bestMove = Directions.STOP

        for (succGameState, succAction) in \
                gameState.generateGhostSuccessors(1):

            succNodeState = hash(make_node_state(succGameState))
            # if succNodeState in self._visited:
            #     continue

            score = self._max_value(succGameState, depth - 1)
            v = min(v, score)
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

                score = self._min_value(succGameState, depth, )

                v = max(v, score)
                bestMove = succAction if v == score else bestMove

            return bestMove

        except Exception as e:
            print(e)

# Make it so that only float are handled in the recursive call.
# Smarty works fine if no visited. Otherwise, doesn't work. Infinite loop
# with the others