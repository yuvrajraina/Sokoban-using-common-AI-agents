import os
from sokoban import State
from queue import PriorityQueue

# get game state based on lvlnumber
def readLevel(lvlnumber,loc='main_levels'):
    f = open(os.path.dirname(__file__) + f"/assets/{loc}/Level_{lvlnumber}.txt")
    lines = f.readlines()
    f.close()
    state = State()
    state.stringInitialize(lines)
    return state

# get a unique hash for the current state
def getHash(state):
    key=str(state.player["x"]) + "," + str(state.player["y"]) + "," + str(len(state.crates)) + "," + str(len(state.targets))
    for c in state.crates:
        key += "," + str(c["x"]) + "," + str(c["y"]);
    for t in state.targets:
        key += "," + str(t["x"]) + "," + str(t["y"]);
    return key

# get the remaining heuristic cost for the current state
def getHeuristic(state):
    targets=[]
    for t in state.targets:
        targets.append(t)
    distance=0
    for c in state.crates:
        bestDist = state.width + state.height
        bestMatch = 0
        for i,t in enumerate(targets):
            if bestDist > abs(c["x"] - t["x"]) + abs(c["y"] - t["y"]):
                bestMatch = i
                bestDist = abs(c["x"] - t["x"]) + abs(c["y"] - t["y"])
        distance += abs(targets[bestMatch]["x"] - c["x"]) + abs(targets[bestMatch]["y"] - c["y"])
        del targets[bestMatch]
    return distance


# initialize deadlock locations where level can't be won from them
def intializeDeadlocks(state):
    sign = lambda x: int(x/max(1,abs(x)))

    state.deadlocks = []
    for y in range(state.height):
        state.deadlocks.append([])
        for x in range(state.width):
            state.deadlocks[y].append(False)

    corners = []
    for y in range(state.height):
        for x in range(state.width):
            if x == 0 or y == 0 or x == state.width - 1 or y == state.height - 1 or state.solid[y][x]:
                continue
            if (state.solid[y-1][x] and state.solid[y][x-1]) or (state.solid[y-1][x] and state.solid[y][x+1]) or (state.solid[y+1][x] and state.solid[y][x-1]) or (state.solid[y+1][x] and state.solid[y][x+1]):
                if not state._checkTargetLocation(x, y):
                    corners.append({"x":x, "y":y})
                    state.deadlocks[y][x] = True

    for c1 in corners:
        for c2 in corners:
            dx,dy = sign(c1["x"] - c2["x"]), sign(c1["y"] - c2["y"])
            if (dx == 0 and dy == 0) or (dx != 0 and dy != 0):
                continue
            walls = []
            x,y=c2["x"],c2["y"]
            if dx != 0:
                x += dx
                while x != c1["x"]:
                    if state._checkTargetLocation(x,y) or state.solid[y][x] or (not state.solid[y-1][x] and not state.solid[y+1][x]):
                        walls = []
                        break
                    walls.append({"x":x, "y":y})
                    x += dx
            if dy != 0:
                y += dy
                while y != c1["y"]:
                    if state._checkTargetLocation(x,y) or state.solid[y][x] or (not state.solid[y][x-1] and not state.solid[y][x+1]):
                        walls = []
                        break
                    walls.append({"x":x, "y":y})
                    y += dy
            for w in walls:
                state.deadlocks[w["y"]][w["x"]] = True

# check if the current state is a deadlock
def checkDeadlock(state):
    if hasattr(state, 'deadlocks'):
        for c in state.crates:
            if state.deadlocks[c["y"]][c["x"]]:
                return True
    return False

directions = [{"x":-1, "y":0}, {"x":1, "y":0}, {"x":0, "y":-1}, {"x":0, "y":1}]

# node class where the agent are using
class Node:
    balance = 0.5
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = 0
        if self.parent != None:
            self.depth = parent.depth + 1

    def getChildren(self):
        children = []
        for d in directions:
            childState = self.state.clone()
            crateMove = childState.update(d["x"], d["y"])
            if childState.player["x"] == self.state.player["x"] and childState.player["y"] == self.state.player["y"]:
                continue
            if crateMove and checkDeadlock(childState):
                continue
            children.append(Node(childState, self, d))
        return children

    def getHash(self):
        return getHash(self.state)

    def getCost(self):
        return self.depth

    def getHeuristic(self):
        return getHeuristic(self.state)

    def checkWin(self):
        return self.state.checkWin()

    def getActions(self):
        actions = []
        current = self
        while(current.parent != None):
            actions.insert(0,current.action)
            current = current.parent
        return actions

    def __str__(self):
        return str(self.depth) + "," + str(self.getHeuristic()) + "\n" + str(self.state)

    def __lt__(self, other):
        return self.getHeuristic()+Node.balance*self.getCost() < other.getHeuristic()+Node.balance*other.getCost()
