from time import sleep

board = [[1, 2, 3, 4, 5, 6],
         [7, 8, 9, 10, 11, 12],
         [13, 14, 15, 16, 17, 18], 
         [19, 20, 21, 22, 23, 24],
         [25, 26, 27, 28, 29, 30],
         [31, 32, 33, 34, 35, 36],
         [37, 38, 39, 40, 41, 42]]

known_obstacles = [[False, False, False, False, False, True],  # position 6 is charging station
                   [False, True, True, False, False, False],    # position 12 is charging station
                   [False, False, False, False, False, False], # position 14 and 15 are loading locations
                   [False, False, False, False, False, False],
                   [False, False, False, False, True, False],  # position 28 is loading location
                   [False, False, False, False, True, False],  # position 31 and 34 is loading location
                   [True, False, False, False, False, False]]  # positon 37 conveyor belt (loading position position 31), 
                                                               

conveyor_belt = {
    "coordinates": (5,0),
    "position": 0
}

charging_station = {
            "coordinates": (0,4),
            "occupied": False
        }


def dijkstra_find_path(board, known_obstacles, start_pos, end_pos):
    rows = len(board)
    cols = len(board[0])

    distances = [[float('inf')] * cols for _ in range(rows)]
    distances[start_pos[0]][start_pos[1]] = 0

    previous_nodes = [[None] * cols for _ in range(rows)]   
    unvisited = set((r, c) for r in range(rows) for c in range(cols) if not known_obstacles[r][c])

    while unvisited:
        current = min(unvisited, key=lambda pos: distances[pos[0]][pos[1]])
        unvisited.remove(current)

        if current == end_pos:
            break

        neighbors = [(current[0] + dr, current[1] + dc) for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
        for neighbor in neighbors:
            r, c = neighbor
            if 0 <= r < rows and 0 <= c < cols and not known_obstacles[r][c] and neighbor in unvisited:
                alt_distance = distances[current[0]][current[1]] + 1
                if alt_distance < distances[r][c]:
                    distances[r][c] = alt_distance
                    previous_nodes[r][c] = current

    # Reconstruct the shortest path
    path = []
    while end_pos is not None:
        path.append(end_pos)
        end_pos = previous_nodes[end_pos[0]][end_pos[1]]
    path.reverse()

    if path[0] != start_pos:
        print("No path found!")
        return []

    return path

def print_board(board, known_obstacles, robots):
    for r in range(len(board)):
        row_display = ""
        for c in range(len(board[0])):
            robotInCell = False
            for robot in robots:
                if (r, c) == robot.getCoordinates():
                    robotInCell = True
                    break
            if robotInCell:
                row_display += " R "
            elif known_obstacles[r][c]:
                row_display += " X "
            else:
                row_display += f" . "
        print(row_display)
    print("\n")


class robot:
    def __init__(self, coordinates, name, battery=100):
        self.name = name
        self.coordinates = coordinates
        self.battery = battery
        self.assigned = False
        self.task = None
        self.pathToPickUp = []
        self.pathToDropOff = []
    
    def getTask(self):
        return self.task
    
    def assignTask(self, task, pathToSource, pathToDestination):
        print(self.name, " is assigned to task")
        self.assigned = True
        self.task = task
        self.pathToPickUp = pathToSource
        self.pathToDropOff = pathToDestination

    def getCoordinates(self):
        return self.coordinates

    def getBattery(self):
        return self.battery
        
    def robotMove(self, coordinates):
        #TODO check for obstacles

        # if obstacle:
        #     do maneuver
        # else:
        if self.battery < len(self.pathToPickUp) + len(self.pathToDropOff) or (self.getBattery() < 11 and self.pathToDropOff[-1] != charging_station["coordinates"]):
            self.pathToPickUp, self.pathToDropOff = requestCharging(self)
        else: 
            self.coordinates = coordinates
            self.battery = self.battery - 1
        

    def pathToPickUp(self):
        return self.pathToPickUp

    def pathToDropOff(self):
        return self.pathToDropOff

    def executeStep(self):
        # are we trying to get to the charging station 
        if len(self.pathToDropOff) != 0 and self.pathToDropOff[-1] == charging_station["coordinates"]:
            self.robotMove(self.pathToDropOff[0])
            self.pathToDropOff = self.pathToDropOff[1:]
            if self.coordinates == charging_station["coordinates"]:
                self.pathToPickUp, self.pathToDropOff = calculatePath(self, self.task)
                self.battery = 100
                print(self.name , " HAS REACHED CHARGING STATION")
            return False
        elif len(self.pathToPickUp) > 0:
            self.robotMove(self.pathToPickUp[0])
            self.pathToPickUp = self.pathToPickUp[1:]
            return False
            # ok we are at the pick up location
        elif not self.task.isPickedUp():
            print(self.pickUp())
            return False
        # we are not going to pick up, we are not going to charge
        elif len(self.pathToDropOff) > 0:
            self.robotMove(self.pathToDropOff[0])
            self.pathToDropOff = self.pathToDropOff[1:]
            return False            
        elif not self.task.isDroppedOff():
            print(self.dropOff())
            return True
        return True 
    
    def pickUp(self):
        self.task.pickUp()
        return self.name + " is picking up box from position "
        
    def dropOff(self):
        self.task.dropOff()
        return self.name + " is dropping off box at position " 


robots = [robot((1,4), "Anne", 10),
          robot((5,5), "Phoebe"),
          robot((0,3), "Sofia"),
          robot((3,4), "Jonatan"),
          robot((1,3), "Janne")]
        

class task:
    def __init__(self, source_coordinates, source_position, destination_coordinates, destination_position):
        self.source_coordinates = source_coordinates
        self.source_position = source_position
        self.destination_coordinates = destination_coordinates
        self.destination_position = destination_position
        self.picked_up = False
        self.dropped_off = False
    
    def getSourceCoordinates(self):
        return self.source_coordinates
    
    def getSourcePosition(self):
        return self.source_position
    
    def getDestinationCoordinates(self):
        return self.destination_coordinates

    def getDestinationPosition(self):
        return self.destination_position

    def isPickedUp(self):
        return self.picked_up
    
    def isDroppedOff(self):
        return self.dropped_off

    def pickUp(self):
        self.picked_up = True

    def dropOff(self):
        self.dropped_off = True


tasks = [
    # Bring a box from the conveyor belt to shelf 8 position p1
    task(conveyor_belt["coordinates"], conveyor_belt["position"], (2,1), 1),
    # Bring a box from shelf 9 position p2 to the conveyor belt
    task((2,2), 2, conveyor_belt["coordinates"], conveyor_belt["position"]),
    #Bring a box from shelf s29 position p3 to shelf s35 position p4
    task((4,3), 3, (5,3), 4),
    # Bring a box from shelf s9 position p1 to the conveyor belt
    task((2,2), 1, conveyor_belt["coordinates"], conveyor_belt["position"]),
    # Bring a box from shelf s8 position p2 to shelf s29 position p1 
    task((2,1), 2, (4,3), 1),
]


def assignRobots():
    for task in tasks:
        for robot in robots:
            if not robot.assigned:
                print("Finding task for ", robot.name)
                (pathToSource, pathToDestination) = calculatePath(robot, task)
                lenTotalPath = len(pathToSource) + len(pathToDestination)
                if lenTotalPath > 0 and lenTotalPath < robot.getBattery():
                    #Assign that robot to task
                    robot.assignTask(task, pathToSource, pathToDestination)
                    break
        print("Couldn't find any robot for this task :((")
                

def calculatePath(robot, task):
    pathToSource = dijkstra_find_path(board, known_obstacles, robot.getCoordinates(), task.getSourceCoordinates())
    pathToDestination = dijkstra_find_path(board, known_obstacles, task.getSourceCoordinates(), task.getDestinationCoordinates())
    return (pathToSource, pathToDestination)
    
def requestCharging(robot):
    print("Robot ", robot.name, " is requesting charging")
    if charging_station["occupied"] == False:
        pathToCharging = dijkstra_find_path(board, known_obstacles, robot.getCoordinates(), charging_station["coordinates"])
        if len(pathToCharging) != 0:
            charging_station["occupied"] = True
            print(robot.name, " found vacant charging station")
            return [], pathToCharging


def execute_tasks():
    done = False
    while (not done):
        done = True
        sleep(1)
        for robot in robots:
            doneRobot = robot.executeStep() 
            # TODO after robot done, what to do with it?
            done = done and doneRobot
        print_board(board,known_obstacles,robots)



def main():
    print("Helllo")
    assignRobots()
    execute_tasks()

if __name__ == "__main__":
    main()