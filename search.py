# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    startState = problem.getStartState()
    goalState = None
    
    # LIFO queue / stack
    # same node can be pushed multiple times to the stack, because LIFO
    stack = util.Stack()
    stack.push(startState)
    
    # map node to tuple (parent, action) for retrieving path
    toParent = {}
    toParent[startState] = (None, None)
    
    # add node when finished processing, popped out of stack
    explored = set()
    explored.add(startState)
    
    
    while not stack.isEmpty():
        v = stack.pop()
        explored.add(v)
        if problem.isGoalState(v):
            goalState = v
            break
        successors = problem.getSuccessors(v)
        for successor in successors:
            #print successor
            successorState = successor[0]
            if not successorState in explored:
                stack.push(successorState)
                toParent[successorState] = (v, successor[1])


    #retrieve path
    actions = []
    if goalState:
        s = goalState
        while toParent[s][1]:
            actions.append(toParent[s][1])
            s = toParent[s][0]
          
    actions.reverse()
    return actions            

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
    startState = problem.getStartState()
    goalState = None
    
    # FIFO queue
    # same node is only pushed once
    queue = util.Queue()
    queue.push(startState)
    
    # map node to (parent, action) for retrieving path
    toParent = {}
    toParent[startState] = (None, None)

    # push node when first visited
    discovered = set()
    discovered.add(startState)
    
    
    while not queue.isEmpty():
        # expand every node in queue
        v = queue.pop()
        if problem.isGoalState(v):
            goalState = v
            break
        successors = problem.getSuccessors(v)
        for successor in successors:
            successorState = successor[0]
            # push when first visited, don't push again in another path
            if not successorState in discovered:
                queue.push(successorState)
                discovered.add(successorState)
                toParent[successorState] = (v, successor[1])    

    #retrieve path
    actions = []
    if goalState:
        s = goalState
        while toParent[s][1]:
            actions.append(toParent[s][1])
            s = toParent[s][0]
           
    actions.reverse()
    return actions 

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"    
    startState = problem.getStartState()
    goalState = None
    
    # priority queue
    # same node can be pushed multiple times
    pqueue = PriorityQueue()
    pqueue.push(startState, 0)
    
    # add node when finished processing
    explored = set()
    explored.add(startState)
    
    # map node to (parent, action, current cost) for retrieving path
    toParent = {}
    toParent[startState] = (None, None, 0)
    
    while not pqueue.isEmpty():
        v, priority = pqueue.pop()
        explored.add(v)
        
        if problem.isGoalState(v):
            goalState = v
            break
        
        successors = problem.getSuccessors(v)
        for successor in successors:
            successorState = successor[0]
            if not successorState in explored:
                cost = priority + successor[2] 

                # if item already exist in queue
                if pqueue.hasItem(successorState):
                    # if old cost is lower, do nothing
                    if cost >= pqueue.getPriority(successorState):
                        continue
                    # remove old item before pushing
                    else:
                        pqueue.removeItem(successorState)
                pqueue.push(successorState, cost)
                # update toParent
                toParent[successorState] = (v, successor[1], cost)

    #retrieve path
    actions = []
    if goalState:
        s = goalState
        while toParent[s][1]:
            actions.append(toParent[s][1])
            s = toParent[s][0]
            
    actions.reverse()
    return actions 
           
                
def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"    
    
    startState = problem.getStartState()
    goalState = None
    
    # priority queue
    # same node can be pushed multiple times
    pqueue = PriorityQueue()
    pqueue.push(startState, heuristic(startState, problem))
    
    # add node when finished processing
    explored = set()
    explored.add(startState)
    
    # map node to (parent, action, current cost) for retrieving path
    toParent = {}
    toParent[startState] = (None, None, 0)
    
    while not pqueue.isEmpty():
        v, priority = pqueue.pop()
        explored.add(v)
        
        if problem.isGoalState(v):
            goalState = v
            break
        
        successors = problem.getSuccessors(v)
        for successor in successors:
            successorState = successor[0]
            if not successorState in explored:
                cost = toParent[v][2] + successor[2] 
                h = heuristic(successorState, problem)
                f = h + cost
                
                # if item already exist in queue
                if pqueue.hasItem(successorState):
                    # if old f is lower, do nothing
                    if f >= pqueue.getPriority(successorState):
                        continue
                    # remove old item before pushing
                    else:
                        pqueue.removeItem(successorState)
                pqueue.push(successorState, f)
                # update toParent
                toParent[successorState] = (v, successor[1], cost)

    #retrieve path
    actions = []
    if goalState:
        s = goalState
        while toParent[s][1]:
            actions.append(toParent[s][1])
            s = toParent[s][0]
            
    actions.reverse()
    return actions 


import heapq
class PriorityQueue:

    def  __init__(self):
        self.heap = []
        self.item_dict = {}

    def push(self, item, priority):

        entry = (priority, item)
        heapq.heappush(self.heap, entry)
        self.item_dict[item] = entry
    
    # pop the smallest
    def pop(self):
        priority, item = heapq.heappop(self.heap)
        if item in self.item_dict and self.item_dict[item][0] == priority:
            del self.item_dict[item]
        return (item, priority)

    def isEmpty(self):
        return len(self.heap) == 0
    
    def removeItem(self, item):
        if not item in self.item_dict:
            raise KeyError("Can't find item.")
        
        priority = self.item_dict[item][0]
        del self.item_dict[item]
        
        self.heap.remove((priority, item))
        heapq.heapify(self.heap)
        
    # return the item with 
    def getPriority(self, item):
        if item in self.item_dict:
            priority = self.item_dict[item][0]
            return priority
        else:
            raise KeyError("Can't find item.")
        
    def hasItem(self, item):
        if item in self.item_dict:
            return True
        else:
            return False
    
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
