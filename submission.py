## ID: 20200725 NAME: Yoon, Seungwoo
######################################################################################
# Problem 2a
# minimax value of the root node: 5
# pruned edges: h, m, t, 1
######################################################################################

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """
  def __init__(self):
    self.lastPositions = []
    self.dc = None


  def getAction(self, gameState):
    """
    getAction chooses among the best options according to the evaluation function.

    getAction takes a GameState and returns some Directions.X for some X in the set {North, South, West, East, Stop}
    ------------------------------------------------------------------------------
    Description of GameState and helper functions:

    A GameState specifies the full game state, including the food, capsules,
    agent configurations and score changes. In this function, the |gameState| argument 
    is an object of GameState class. Following are a few of the helper methods that you 
    can use to query a GameState object to gather information about the present state 
    of Pac-Man, the ghosts and the maze.
    
    gameState.getLegalActions(): 
        Returns the legal actions for the agent specified. Returns Pac-Man's legal moves by default.

    gameState.generateSuccessor(agentIndex, action): 
        Returns the successor state after the specified agent takes the action. 
        Pac-Man is always agent 0.

    gameState.getPacmanState():
        Returns an AgentState object for pacman (in game.py)
        state.configuration.pos gives the current position
        state.direction gives the travel vector

    gameState.getGhostStates():
        Returns list of AgentState objects for the ghosts

    gameState.getNumAgents():
        Returns the total number of agents in the game

    gameState.getScore():
        Returns the score corresponding to the current state of the game
        It corresponds to Utility(s)

    
    The GameState class is defined in pacman.py and you might want to look into that for 
    other helper methods, though you don't need to.
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best


    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    return successorGameState.getScore()


def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

######################################################################################
# Problem 1a: implementing minimax

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (problem 1)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction. Terminal states can be found by one of the following: 
      pacman won, pacman lost or there are no legal moves. 

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game

      gameState.getScore():
        Returns the score corresponding to the current state of the game
        It corresponds to Utility(s)
    
      gameState.isWin():
        Returns True if it's a winning state
    
      gameState.isLose():
        Returns True if it's a losing state

      self.depth:
        The depth to which search should continue
    """   
    
    # BEGIN_YOUR_ANSWER (our solution is 30 lines of code, but don't worry if you deviate from this)
    
    def value(gameState,cLevel,depth=self.depth):
      """calculate (value,action) of the tree-node 
         
         cLevel : current level of tree searching, starting from 1
         depth  : self.depth
      """
      if cLevel==depth*(self.numAgent) + 1 or gameState.isWin() or gameState.isLose():
        return (self.evaluationFunction(gameState),)
      elif (cLevel-1)%(self.numAgent) == 0:
        #MaxNode
        return maxValue(gameState,cLevel)
      else:
        return minValue(gameState,cLevel)
      
    def maxValue(gameState,cLevel):
      """return (score,action) tuple, where score is maximum utility values among utility values of successors
         and action is the action that results in the max score
      """
      legalMoves = gameState.getLegalActions(0)
      successorStates = [gameState.generateSuccessor(0, action) for action in legalMoves]
      scores = [value(successorState,cLevel+1)[0] for successorState in successorStates]
      maxScore=max(scores)
      bestIndex = scores.index(maxScore)
      maxAction = legalMoves[bestIndex]
      return (maxScore,maxAction)
    
    def minValue(gameState,cLevel):
      """return (score,action) tuple, where score is minimum utility values among utility values of successors
         and action is the action that results in the min score
      """
      agentIndex = ( (cLevel-1) % (self.numAgent) )
      legalMoves = gameState.getLegalActions(agentIndex)
      successorStates = [gameState.generateSuccessor(agentIndex, action) for action in legalMoves]
      scores = [value(successorState,cLevel+1)[0] for successorState in successorStates]
      minScore=min(scores)
      bestIndex = scores.index(minScore)
      minAction = legalMoves[bestIndex]
      return (minScore,minAction)

    self.numAgent=gameState.getNumAgents() #number of agents
    (score,action)=value(gameState,1)
    return action
    # END_YOUR_ANSWER

######################################################################################
# Problem 2b: implementing alpha-beta

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (problem 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """

    # BEGIN_YOUR_ANSWER (our solution is 42 lines of code, but don't worry if you deviate from this)
    def value(gameState,cLevel,alpha,beta,depth=self.depth):
      """calculate (value,action) of the tree-node 
         
         cLevel : current level of tree searching, starting from 1
         depth  : self.depth
      """
      if cLevel==depth*(self.numAgent) + 1 or gameState.isWin() or gameState.isLose():
        return (self.evaluationFunction(gameState),)
      elif (cLevel-1)%(self.numAgent) == 0:
        #MaxNode
        return maxValue(gameState,cLevel,alpha,beta)
      else:
        return minValue(gameState,cLevel,alpha,beta)
      
    def maxValue(gameState,cLevel,alpha,beta):
      """return (score,action) tuple, where score is maximum utility values among utility values of successors
         and action is the action that results in the max score
      """
      maxScore=float("-inf")
      legalMoves = gameState.getLegalActions(0)
      for action in legalMoves:
        successorState = gameState.generateSuccessor(0, action)
        score = value(successorState,cLevel+1,alpha,beta)[0]
        if score>=beta :
          #done
          return (score,action)
        elif score>maxScore:
          maxScore=score
          maxAction = action
          alpha=score if score > alpha else alpha
      return (maxScore,maxAction)
    
    def minValue(gameState,cLevel,alpha,beta):
      """return (score,action) tuple, where score is minimum utility values among utility values of successors
         and action is the action that results in the min score
      """
      minScore=float("inf")
      agentIndex = ( (cLevel-1) % (self.numAgent) )
      legalMoves = gameState.getLegalActions(agentIndex)
      for action in legalMoves:
        successorState = gameState.generateSuccessor(agentIndex, action)
        score = value(successorState,cLevel+1,alpha,beta)[0]
        if score<=alpha :
          #done
          return (score,action)
        elif score<minScore:
          minScore=score
          minAction = action
          beta=score if score < beta else beta
      return (minScore,minAction)

    self.numAgent=gameState.getNumAgents() #number of agents
    (score,action)=value(gameState,1,float("-inf"),float("inf"))
    return action
    # END_YOUR_ANSWER

######################################################################################
# Problem 3a: implementing expectimax

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (problem 3)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """

    # BEGIN_YOUR_ANSWER (our solution is 30 lines of code, but don't worry if you deviate from this)
    def value(gameState,cLevel,depth=self.depth):
      """calculate (value,action) of the tree-node 
         
         cLevel : current level of tree searching, starting from 1
         depth  : self.depth
      """
      if cLevel==depth*(self.numAgent) + 1 or gameState.isWin() or gameState.isLose():
        return (self.evaluationFunction(gameState),)
      elif (cLevel-1)%(self.numAgent) == 0:
        #MaxNode
        return maxValue(gameState,cLevel)
      else:
        #exp node
        return expValue(gameState,cLevel)
      
    def maxValue(gameState,cLevel):
      """return (score,action) tuple, where score is maximum utility values among utility values of successors
         and action is the action that results in the max score
      """
      legalMoves = gameState.getLegalActions(0)
      successorStates = [gameState.generateSuccessor(0, action) for action in legalMoves]
      scores = [value(successorState,cLevel+1)[0] for successorState in successorStates]
      maxScore=max(scores)
      bestIndex = scores.index(maxScore)
      maxAction = legalMoves[bestIndex]
      return (maxScore,maxAction)
    
    def expValue(gameState,cLevel):
      """return (score,action) tuple, where score is expectation of utility values over successors
         and action is the action that results in the min score
      """
      agentIndex = ( (cLevel-1) % (self.numAgent) )
      legalMoves = gameState.getLegalActions(agentIndex)
      successorStates = [gameState.generateSuccessor(agentIndex, action) for action in legalMoves]
      scores = [value(successorState,cLevel+1)[0] for successorState in successorStates]
      expScore=sum(scores)/len(scores)
      action = legalMoves[0] # the return value 'action' does not matter in exp node. Pacman agent get action from max node.
      return (expScore,action)

    self.numAgent=gameState.getNumAgents() #number of agents
    (score,action)=value(gameState,1)
    return action
    # END_YOUR_ANSWER

######################################################################################
# Problem 4a (extra credit): creating a better evaluation function

def betterEvaluationFunction(currentGameState):
  """
  Your extreme, unstoppable evaluation function (problem 4).
  """

  # BEGIN_YOUR_ANSWER (our solution is 60 lines of code, but don't worry if you deviate from this)
  score=currentGameState.getScore()
  foodList=currentGameState.getFood()
  capsulePositions=currentGameState.getCapsules() #getCapsule returns positions of remaining capsules
  capsuleDistances=[] #distances between pacman and capsules
  foodDistances=[] #distances between pacman and foods
  
  posX=currentGameState.getPacmanPosition()[0]
  posY=currentGameState.getPacmanPosition()[1]

  for x in range(currentGameState.data.layout.width):
    for y in range(currentGameState.data.layout.height):
      if foodList[x][y]==1:
        distance=((posX-x)**2+(posY-y)**2)**0.5
        foodDistances.append(distance)

        
  if foodDistances:    #when list is not empty
    minFoodDistance=min(foodDistances)
  else:
    minFoodDistance=0
  """
  if capsulePositions:    #when list is not empty
    for i in range(len(capsulePositions)):
      distance=((posX-capsulePositions[i][0])**2+(posY-capsulePositions[i][1])**2)**0.5
      capsuleDistances.append(distance)
    minCapsuleDistance=min(capsuleDistances)
  else:
    minCapsuleDistance=0
  """
  
  numRemainedCapsules=len(capsulePositions)
        
  direction=currentGameState.getPacmanState().getDirection()
  if direction==Directions().NORTH or direction==Directions().EAST:
    score+=10   #for tiebreaking, add some additional score to certain direction

  score-=minFoodDistance
  score-=numRemainedCapsules*100
  foodDistances.clear()
  capsuleDistances.clear()
  score-=currentGameState.getNumFood()

  return score
  # END_YOUR_ANSWER

# Abbreviation
better = betterEvaluationFunction

