# Sokoban Environment - NYU CS-GY6613
---
## Prerequisites
Requires python3 to run
##### Install libraries
`$ pip install -r requirements.txt`
## Run the Game

##### Solve as a human
`$ python3 game.py --play`
`$ python3 game.py --agent Human`
##### Solve with an agent
`$ python3 game.py --agent [AGENT-NAME-HERE]`

`$ python3 game.py --agent BFS #run game with BFS agent`

`$ python3 game.py --agent AStar --no_render #run game with AStar agent without rendering`

## Parameters
`--play` - run the game as a human player

`--no_render` - run the AI solver without showing the game screen 

`--agent [NAME]`  - the type of agent to use [Human, DoNothing, Random, BFS, DFS, AStar, HillClimber, Genetic, MCTS]

`--level [#]` - which level to test (0-99) or 'random' for a randomly selected level that an agent can solve in at most 2000 iterations. These levels can be found in the 'assets/gen_levels/' folder (default=0)

`--iterations [#]` - how many iterations to allow the agent to search for (default=3000)

`--solve_speed [#]` - how fast (in ms) to show each step of the solution being executed on the game screen 
## Code Functions 
_These are the only functions you need to concern yourselves with to complete the assignments._
**WARNING: DO NOT MODIFY THESE FUNCTIONS!**

#### Sokoban_py
* **state.clone()** - creates a full copy of the current state (for use in initializing Nodes or for feedforward simulation of states without modifying the original) **Use with HillClimber to test sequences**
* **state.checkWin()** - checks if the game has been won in this state _(return type: bool)_
* **state.update(x,y)** - updates the state with the given direction in the form _x,y_ where _x_ is the change in x axis position and _y_ is the change in y axis position. Used to feed-forward a state. **Use with HillClimber Agent to test sequences.**


#### Agent_py
* **Agent()** - base class for the Agents
* **RandomAgent()** - agent that returns list of 20 random directions
* **DoNothingAgent()** - agent that makes no movement for 20 steps

* **BFSAgent()** - agent that solves the level using Breadth First Search
* **DFSAgent()** - agent that solves the level using Depth First Search
* **AStarAgent()** - agent that solves the level using A* Search
* **HillClimberAgent()** - agent that solves the level using HillClimber Search algorithm
* **GeneticAgent()** - agent that solves the level using Genetic Search algorithm
* **MCTSAgent()** - agent that solves the level using Monte Carlo Tree Search algorithm

#### Helper_py
* **Other functions**
   * **getHeuristic(state)** - returns the remaining heuristic cost for the current state - a.k.a. distance to win condition (return type: int). **Use with HillClimber Agent to compare states at the end of sequence simulations**
   * **directions** - list of all possible directions (x,y) the agent/player can take **Use with HillClimber Agent to mutate sequences**

* **Node Class**
   * **\_\_init\_\_(state, parent, action)** - where _state_ is the current layout of the game map, _parent_ is the Node object preceding the state, and _action_ is the dictionary XY direction used to reach the state _(return type: Node object)_
   * **checkWin()** - returns if the game is in a win state where all of the goals are covered by crates _(return type: bool)_
   * **getActions()** - returns the sequence of actions taken from the initial node to the current node _(return type: str list)_
   * **getHeuristic()** - returns the remaining heuristic cost for the current state - a.k.a. distance to win condition _(return type: int)_
   * **getHash()** - returns a unique hash for the current game state consisting of the positions of the player, goals, and crates made of a string of integers - for use of keeping track of visited states and comparing Nodes _(return type: str)_
   * **getChildren()** - retrieves the next consecutive Nodes of the current state by expanding all possible directional actions _(return type: Node list)_
   * **getCost()** - returns the depth of the node in the search tree _(return type: int)_

* **MCTSNode Class (extension of Node() for use with the MCTSAgent only)**
   *  **\_\_init\_\_(state, parent, action, maxDist)** - modified to include variable to keep track of number of times visited _(self.n)_, variable to keep track of score _(self.q)_, and variable to keep make score value larger as solution gets nearer _(self.maxDist)_
   *  **getChildren(visited)** - returns the node's children if already made - otherwise creates new children based on whether states have been visited yet and saves them for use later _(self.children)_ 
   *  **calcEvalScore(state)** - calculates the evaluation score for a state compared to the node by examining the heurstic value compared to the starting heuristic value (larger = better = higher score) - for use with the rollout and general MCTS algorithm functions



## FAQs
* _What is `iterations` and `max_iterations`?_
    * `iterations` keeps track of how many nodes you can expand upon in the tree, and `max_iterations` is the number of nodes you are allowed to search. In the case of evolutionary search, this is the number of times the solution is allowed to evolve. This variable is implemented to prevent infinite loops from occuring in case your algorithm has an error. Each level in the Sokoban framework should be able to be solved in 3000 iterations (the default number) or less for every AI solver.
* _Can I use other libraries?_
    * No. All the functions you need are already included in the code template. Do not import any internal or external libraries for any reason. 
* _I get infinite loops / My agent is running in circles. / My agent keeps going back to the same place._
    * Make sure you are using __`node_a.getHash() == node_b.getHash()`__ to check the equivalency of 2 nodes and NOT `node_a == node_b`
* _Is it ok if my agent's solution is less than 50 steps but returned a solution length of 50 anyways?_
    * Yes, as long as it reaches the win state of the level.
* _My Hillclimber/MCTS Agent doesn't win the level, is this ok?_
    * That's fine, as long as the final solution gets somewhat close to the win state. Because of the stochastic nature of Hillclimber and MCTS, around 70\%-80\% of levels should be solved. 


