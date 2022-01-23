#########################################
#                                       #
#                                       #
#  ==  SOKOBAN STUDENT AGENT CODE  ==   #
#                                       #
#      written by: [YUVRAJ RAINA]       #
#                                       #
#                                       #
#########################################


# SOLVER CLASSES wHERE AGENT CODES GO
from helper import *
import random
import math


# Base class of agent (DO NOT TOUCH!)
class Agent:
    def getSolution(self, state, maxIterations):

        '''
        EXAMPLE USE FOR TREE SEARCH AGENT:


        #expand the tree until the iterations runs out or a solution sequence is found
        while (iterations < maxIterations or maxIterations <= 0) and len(queue) > 0:
            iterations += 1

            [ POP NODE OFF OF QUEUE ]

            [ EVALUATE NODE AS wIN STATE]
                [ IF wIN STATE: BREAK AND RETURN NODE'S ACTION SEQUENCE]

            [ GET NODE'S CHILDREN ]

            [ ADD VALID CHILDREN TO QUEUE ]

            [ SAVE CURRENT BEST NODE ]


        '''


        '''
        EXAMPLE USE FOR EVOLUTION BASED AGENT:
        #expand the tree until the iterations runs out or a solution sequence is found
        while (iterations < maxIterations or maxIterations <= 0) and len(queue) > 0:
            iterations += 1

            [ MUTATE ]

            [ EVALUATE ]
                [ IF wIN STATE: BREAK AND RETURN ]

            [ SAVE CURRENT BEST ]

        '''


        return []       # set of actions


#####       EXAMPLE AGENTS      #####

# Do Nothing Agent code - the laziest of the agents
class DoNothingAgent(Agent):
    def getSolution(self, state, maxIterations):
        if maxIterations == -1:     # RIP your machine if you remove this block
            return []

        #make idle action set
        nothActionSet = []
        for i in range(20):
            nothActionSet.append({"x":0,"y":0})

        return nothActionSet

# Random Agent code - completes random actions
class RandomAgent(Agent):
    def getSolution(self, state, maxIterations):
        #make random action set
        randActionSet = []
        for i in range(20):
            randActionSet.append(random.choice(directions))
            
        return randActionSet




#####    ASSIGNMENT 1 AGENTS    #####


# BFS Agent code
class BFSAgent(Agent):
    def getSolution(self, state, maxIterations=-1):
        intializeDeadlocks(state)
        iterations = 0
        bestNode = None
        queue = [Node(state.clone(), None, None)]
        visited = []

        #expand the tree until the iterations runs out or a solution sequence is found
        while (iterations < maxIterations or maxIterations <= 0) and len(queue) > 0:
            curr_node=queue.pop(0)
            #check win condition
            if curr_node.checkwin()==True:
                # return win state
                bestNode=curr_node
                break
            # find all possible moves for current state
            moves=curr_node.getChildren()
            #here notice that we save the visited elements for all
            #unlike DFS that will store only the first element that was visited
            #and iterate ove it till depth was completely found or solution was found
            for i in moves:
                if i.getHash() in visited:
                    continue
                else:
                    visited.append(i.getHash())
                    queue.append(i)
            iterations += 1

        if bestNode == None:
            return 'Solution Not Found'                       #remove me
        else:
            return bestNode.getActions()   #uncomment me


# DFS Agent Code
class DFSAgent(Agent):
    def getSolution(self, state, maxIterations=-1):
        intializeDeadlocks(state)
        iterations = 0
        bestNode = None
        queue = [Node(state.clone(), None, None)]
        visited = []
        
        #expand the tree until the iterations runs out or a solution sequence is found
        while (iterations < maxIterations or maxIterations <= 0) and len(queue) > 0:
            
            curr_node=queue.pop()
            # append the current node as visited node
            # appending only once out of next loop allows to discard all paths that were
            # not to be sorted hence only iterating and storing the fixed path to be taken
            visited.append(curr_node.getHash())
            #check win condition
            if curr_node.checkwin()==True:
                #return as solution
                bestNode=curr_node
                break
            # save all possible moves
            moves=curr_node.getChildren()
            for i in moves:
                if i.getHash() in visited:
                    continue
                else:
                    # instead of appending here we only iterate through it once
                    #visited.append(i.getHash())
                    queue.append(i)
                    
            iterations += 1
        if bestNode == None:
            return 'Solution Not Found'                       #remove me
        else:
            return bestNode.getActions()   #uncomment me



# AStar Agent Code
class AStarAgent(Agent):
    def getSolution(self, state, maxIterations=-1):
        #setup
        intializeDeadlocks(state)
        iterations = 0
        bestNode = None

        #initialize priority queue
        queue = PriorityQueue()
        # need to initialize total cost as 0 for start
        queue.put(Node(state.clone(), None, 0),0)
        visited = []
        
        
        

        while (iterations < maxIterations or maxIterations <= 0) and queue.qsize() > 0:
            
            
            curr_node=queue.get()
            
            # save children of the current node
            moves=curr_node.getChildren()
            
            # iterate for all children such that total cost= heuristic cost + cost of depth
            for i in moves:
                total_cost= i.getHeuristic()+i.getCost()
                # append in visited hash table
                # and put in queue as next element
                # note priorityqueue will itself sort on basis of total_cost
                
                
                if i.checkwin()==True:
                    #return as solution
                    if bestNode==None:
                        bestNode=i
                    elif bestNode.__lt__(i):
                        bestNode=curr_node
                        if i.getHash() not in visited:
                            visited.append(i.getHash())
                            queue.put(i,total_cost)
                
                
                
                
            iterations += 1

            



        if bestNode == None:
            return []                       #remove me
        else:
            return bestNode.getActions()   #uncomment me


#####    ASSIGNMENT 2 AGENTS    #####


# Hill Climber Agent code
class HillClimberAgent(Agent):
    
            
    
    def getSolution(self, state, maxIterations=-1):
        #setup
        intializeDeadlocks(state)
        iterations = 0
        
        seqLen = 50            # maximum length of the sequences generated
        coinFlip = 0.5          # chance to mutate
        node = state
        #initialize the first sequence (random movements)
        bestSeq = []
        # create seq with random directions
        for i in range(seqLen):
            bestSeq.append(random.choice(directions))
        # get state to check possible outcomes
        state_clone=state.clone()
        # initial setup
        for i in bestSeq:
            state_clone.update(i["x"],i["y"])
        state_clone=Node(state_clone.clone(),None,None)
        cost = state_clone.getHeuristic()
        if state_clone.checkwin()==True:
            return bestSeq
        # cost will store the heuristic and will be helping to find the maxima
        
        #mutate the best sequence until the iterations runs out or a solution sequence is found
        while (iterations < maxIterations):
            temp_seq= bestSeq
            temp_state=state.clone()
            for i in range(len(temp_seq)):
                if random.randint(0,1)>coinFlip:
                    temp_seq[i]=random.choice(directions)
            # if cost after updating is lower then select the new sequence
            for i in temp_seq:
                temp_state.update(i["x"],i["y"])
            temp_state=Node(temp_state.clone(),None,None)
            if cost > temp_state.getHeuristic():
                cost=temp_state.getHeuristic()
                bestSeq=temp_seq
            if cost==0:
                break
            
            iterations+=1
            ## YOUR CODE HERE ##




        #return the best sequence found
        return bestSeq  



# Genetic Algorithm code
class GeneticAgent(Agent):
    def getSolution(self, state, maxIterations=-1):
        #setup
        intializeDeadlocks(state)

        iterations = 0
        seqLen = 50             # maximum length of the sequences generated
        popSize = 10            # size of the population to sample from
        parentRand = 0.5        # chance to select action from parent 1 (50/50)
        mutRand = 0.3           # chance to mutate offspring action

        bestSeq = []            #best sequence to use in case iterations max out

        #initialize the population with sequences of POP_SIZE actions (random movements)
        population = []
        for p in range(popSize):
            for i in range(seqLen):
                bestSeq.append(random.choice(directions))
            population.append(bestSeq)

        #mutate until the iterations runs out or a solution sequence is found
        while (iterations < maxIterations):
            iterations += 1
            cur_state = state.clone()
            population_sorted = []

			for p in range(popSize):
               	cur_state = state.clone()
                for s in population[p]:
                    cur_state.update(s['x'], s['y'])
                if (cur_state.checkwin()):
                    bestSeq = population[p]
                    return bestSeq

                population_sorted.append((get_heuristic(cur_state), population[p]))

            population_sorted.sort(key=lambda i: i[0])

            if (population_sorted[0][0] < getHeuristic(state)):
                bestSeq = population_sorted[0][1]

            new_pop = []
            for i in range(popSize//2)):

                phase1 = population_sorted[random.randint(0, popSize)][1]
                phase2 = population_sorted[random.randint(0, popSize)][1]

                offspring = []
                if (random.randint(0,1) < parentRand):
                    offspring = (phase1[0:len(phase1)/2] + phase2[len(phase2)/2:len(phase2)])
                else:
                    offspring = (phase2[0:len(phase2)/2] + phase1[len(phase1)/2:len(phase1)])

                for i in range(50):
                    if (random.randint(0,1) < mutRand):
                        offspring[i] = random.choice(directions)


                new_pop.append(offspring)



            for i in range(int(popSize/2)):
                new_pop.append(population_sorted[i][1])

            population = new_pop

        return bestSeq


class MCTSNode(Node):
    def __init__(self, state, parent, action, maxDist):
        super().__init__(state,parent,action)
        self.children = []  #keep track of child nodes
        self.n = 0          #visits
        self.q = 0          #score
        self.maxDist = maxDist      #starting distance from the goal (heurstic score of initNode)

    #update get children for the MCTS
    def getChildren(self,visited):
        #if the children have already been made use them
        if(len(self.children) > 0):
            return self.children

        children = []

        #check every possible movement direction to create another child
        for d in directions:
            childState = self.state.clone()
            crateMove = childState.update(d["x"], d["y"])

            #if the node is the same spot as the parent, skip
            if childState.player["x"] == self.state.player["x"] and childState.player["y"] == self.state.player["y"]:
                continue

            #if this node causes the game to be unsolvable (i.e. putting crate in a corner), skip
            if crateMove and checkDeadlock(childState):
                continue

            #if this node has already been visited (same placement of player and crates as another seen node), skip
            if getHash(childState) in visited:
                continue

            #otherwise add the node as a child
            children.append(MCTSNode(childState, self, d, self.maxDist))

        self.children = list(children)    #save node children to generated child

        return children

    #calculates the score the distance from the starting point to the ending point (closer = better = larger number)
    def calcEvalScore(self,state):
        return self.maxDist - getHeuristic(state)

    #compares the score of 2 mcts nodes
    def __lt__(self, other):
        return self.q < other.q

    #print the score, node depth, and actions leading to it
    #for use with debugging
    def __str__(self):
        return str(self.q) + ", " + str(self.n) + ' - ' + str(self.getActions())


# Monte Carlo Tree Search Algorithm code
class MCTSAgent(Agent):
    def getSolution(self, state, maxIterations=-1):
        #setup
        intializeDeadlocks(state)
        iterations = 0
        bestNode = None
        initNode = MCTSNode(state.clone(), None, None, getHeuristic(state))

        while(iterations < maxIterations):
            #print("\n\n---------------- ITERATION " + str(iterations+1) + " ----------------------\n\n")
            iterations += 1

            #mcts algorithm
            rollNode = self.treePolicy(initNode)
            score = self.rollout(rollNode)
            self.backpropogation(rollNode, score)

            #if in a win state, return the sequence
            if(rollNode.checkwin()):
                return rollNode.getActions()

            #set current best node
            bestNode = self.bestChildUCT(initNode)
            

            #if in a win state, return the sequence
            if(bestNode and bestNode.checkwin()):
                return bestNode.getActions()


        #return solution of highest scoring descendent for best node
        #if this line was reached, that means the iterations timed out before a solution was found
        return self.bestActions(bestNode)
        

    #returns the descendent with the best action sequence based
    def bestActions(self, node):
        #no node given - return nothing
        if node == None:
            return []

        bestActionSeq = []
        while(len(node.children) > 0):
            node = self.bestChildUCT(node)

        return node.getActions()


    ####  MCTS SPECIFIC FUNCTIONS BELOw  ####

    #determines which node to expand next
    def treePolicy(self, rootNode):
        curNode = rootNode
        visited = []
        # create state clone from node for  working 
        state_clone=curNode.state.clone()
        # if root not visited first visit root itself
        if curNode.n ==0:
            return curNode
        # for every node selected using best child UCT select the node with less sore if all are visited or select the node that has not been visited repeat until reach leaf and die 
        while state_clone.checkwin()==False:
            
            #visited.append(getHash(curNode.state))
            temp = curNode.getChildren(visited)
            for i in temp:
                if i.n==0:
                    return i
            curNode = self.bestChildUCT(curNode)
            if curNode!=None:
                state_clone=curNode.state.clone()
            if curNode==None:
                return rootNode
        return curNode
 
    # uses the exploitation/exploration algorithm
    def bestChildUCT(self, node):
        c = 1    #c value in the exploration/exploitation equation
        bestChild = None
        bestAction=[-1,None]
        
        # best  action [0] stores cost [1] stores child
        for i in node.children:
            temp=i.state.clone()
            if temp.checkwin()==True:
                return i
            # if first visit return node as score is infinite
            # this step alsoo makes sure that no 0 are fed in denominator
            if i.n==0:
                return i
            result = (i.q/i.n) + (c*(math.sqrt((2*math.log(node.n))/i.n)))
            
            
            
            if result == bestAction[0]:
                bestAction[1]=i
            if result > bestAction[0]:
                bestAction = [result,i]
        
        # if leaf reached then return the leaf
        if bestAction[1]==None:
            return node.parent
        else:
         
            return bestAction[1]
            
        



     #simulates a score based on random actions taken
    def rollout(self,node):
        
        numRolls = 7
        # rollout ensure we go 7 steps in some direction and return what we find there
        # if at any point during rollout we find a win state break rollout and return that state
        temp = node.state.clone()
        for i in range(numRolls):
            action = random.choice(directions)
            temp.update(action['x'], action['y'])
            
            if (temp.checkwin()):
                score = node.calcEvalScore(temp)
                return score

        score = node.calcEvalScore(temp)
        return score




     #updates the score all the way up to the root node
    def backpropogation(self, node, score):
        while(node!=None):
            
            # update time visited, score and bact to parent until no node furthur to be calculated
            node.n+=1
            node.q+=score
            node=node.parent

        return
        

