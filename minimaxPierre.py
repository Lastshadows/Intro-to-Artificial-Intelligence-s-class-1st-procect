# Complete this class for all parts of the project

from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module import util
from pacman_module import layout
from pacman_module import pacman as doc

def terminal_test(gameState, depth)->bool:
    # leaf node or end of game
    return depth <= 0 or gameState.isWin() or gameState.isLose()


def make_node_state(gameState):
    # return (hash(gameState.getPacmanPosition()),
    #         hash(gameState.getFood()), hash(tuple(gameState.getGhostStates())))
    return (hash(gameState.getPacmanPosition()),
            hash(gameState.getFood()), hash(tuple(gameState.getGhostStates())))


class PacmanAgent(Agent):

    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args

        # The last element of the path is the state of a node
        self._fringe = util.PriorityQueue()

        # Stores the sequence of moves to perform
        self._moveSeq = None

        # Stores the already explored nodes.
        # Set because hash functions are faster to retrieve an element (O(1))
        self._visited = set()

    def _utilFct(self, gameState)->float:
         if gameState.isWin():
             return 1
         else:
             return -1
        #return float(gameState.getScore())

    def _max_value(self, gameState, depth)->(float, doc.GameState):

        if depth == 0:
            #if we have reached our max depth
            print("[max_value] depth reached ! ")
            return gameState.getScore(), gameState

        if terminal_test(gameState, depth):
            print("[max_value] Terminal node reached")
            print("depth : {}\n \n is Win ? {} \n \n is Lost ? : {} ".format(depth, gameState.isWin(), gameState.isLose()))
            return self._utilFct(gameState), gameState

        v = float("-inf")
        nextState = None

        for (succGameState, succAction) in \
                gameState.generatePacmanSuccessors():

            print("[max_value]Successor ({}):".format(succAction))
            #print(succGameState)

            succNodeState = hash(make_node_state(succGameState))
            if succNodeState in self._visited:
                print("[max_value] This state has already been visited")
                continue

            self._visited.add(succNodeState)

            vMin, stateMin = self._min_value(succGameState, depth)
            print("[max_value]End of call min_value: StateMin=")
            #print(stateMin)
            print("[max_value]vmin = {}".format(vMin))

            v = max(v, vMin)
            nextState = stateMin if v == vMin else nextState
            print("[max_value] Next state is")
            #print(nextState)

        # Everything already visited: avoid loop
        if nextState is None:
            # because called by min_value, it should not be taken in the min(
            # v, max_value())
            print("[max_value] NextState is None -> avoid loop")
            return float("+inf"), None
        print("[max_value] append {} in visited".format(
            nextState.getPacmanState().getDirection()))
        self._moveSeq.append(nextState.getPacmanState().getDirection())

        return v, nextState

    def _min_value(self, gameState, depth)->(float, doc.GameState):

        if depth == 0:
            #if we have reached our max depth
            print("[min_value] depth reached ! ")
            return gameState.getScore(), gameState

        if terminal_test(gameState, depth):
            print("[min_value] Terminal node reached")
            return self._utilFct(gameState)

        v = float("+inf")
        nextState = None

        for (succGameState, succAction) in \
                gameState.generateGhostSuccessors(1):

            print("[min_value]Successor ({}):".format(succAction))
            #print(succGameState)

            succNodeState = hash(make_node_state(succGameState))
            if succNodeState in self._visited:
                print("[min_value] This state has already been visited")
                continue

            vMax, stateMax = self._max_value(succGameState, depth)
            print("[min_value]End of call max_value: StateMax=")
            #print(stateMax)
            print("[min_value]vmax !!! = {}".format(vMax))
            print("[min_value]v !!! = {}".format(v))
            v = min(v, vMax)
            nextState = stateMax if v == vMax else nextState

        # Everything already visited: avoid loop
        if nextState is None:
            # because called by min_value, it should not be taken in the max(
            # v, min_value())
            print("[min_value] NextState is None -> avoid loop")
            return float("-inf"), None
        print("[min_value] append {} in visited".format(
            nextState.getPacmanState().getDirection()))

        return v, nextState


    # def _old_min_value(self, gameState, depth)->int:
    #     if terminal_test(gameState, depth):
    #         return self._utilFct(gameState)
    #
    #     v = float("+inf")
    #
    #     for (succGameState, succAction) in gameState.generateGhostSuccessors():
    #         succNodeState = hash(make_node_state(succGameState))
    #         if succNodeState in self._visited:
    #             continue # ou v= -infty
    #
    #         v = min(v, self._max_value(succGameState, depth))
    #     return v

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
        depth = 1
        try:
            # First call to get_action
            if self._moveSeq is None:

                if state.getNumAgents() - 1 != 1:
                    raise Exception("One ghost is expected: not more nor "
                                    "less !")

                self._moveSeq = []

                self._max_value(state, depth)
                # In order to just pop() the next dir. at each future call

                self._moveSeq.reverse()
        except Exception as e:
            print(e)

        if len(self._moveSeq) == 0:
            print("ERROR: move sequence is empty but game not won nor lost")
            return Directions.STOP

        return self._moveSeq.pop()
